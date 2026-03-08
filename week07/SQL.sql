/* ------------------------------------------------------------
   Build base dataset of highway statistics by joining multiple
   source tables containing traffic counts, road metadata,
   weather risk, and incident data.
-------------------------------------------------------------*/
with highway_stats as (

    select  traffic.segment_id,
            aadt_total,                 -- total annual average daily traffic
            aadt_ev,                    -- estimated EV traffic
            aadt_truck,                 -- truck traffic volume
            peak_factor,                -- congestion indicator
            segment.interstate,
            segment.lanes,
            segment.speed_limit,
            
            risk_score,                 -- weather-related risk score
            
            crash_rate, 
            incident_rate,              -- safety indicators
    
            /* Calculate EV share of traffic */
            (traffic.aadt_ev / traffic.aadt_total) * 100 as ev_percentage,

            /* Calculate truck share of traffic */
            (traffic.aadt_truck / traffic.aadt_total) * 100 as truck_percentage
    
    from    data5035.spring26.traffic_counts as traffic
    
            /* Join road characteristics */
            join data5035.spring26.road_segments as segment
                on segment.segment_id = traffic.segment_id
            
            /* Weather risk associated with the segment */
            left join data5035.spring26.weather_risk as weather
                on weather.segment_id = traffic.segment_id 
        
            /* Historical incident data */
            left outer join data5035.spring26.incidents as i
                on i.segment_id = segment.segment_id 

),

/* ------------------------------------------------------------
   Identify environmental constraints.
   Count wetlands within 1km of each road segment using spatial
   proximity (ST_DWITHIN).
-------------------------------------------------------------*/
wetland_areas as ( 
    select  r.segment_id,
            count(w.constraint_id) as wetlands_nearby
    from    data5035.spring26.road_segments r
            left join data5035.spring26.env_constraints w
                on ST_DWITHIN(r.geom, w.geom, 1000) -- 1 km environmental buffer
    group   by r.segment_id
),

/* ------------------------------------------------------------
   Calculate distance from each road segment to every
   interchange in the dataset.
-------------------------------------------------------------*/
distances as ( 
    select  s.segment_id,
            i.interchange_id, 
            st_distance(
                s.geom,
                i.geom
            ) / 1000 as distance_km
    from    data5035.spring26.road_segments s
            cross join data5035.spring26.interchanges i   
),

/* ------------------------------------------------------------
   Rank segments by proximity to each interchange so we can
   identify which segment is closest to each interchange.
-------------------------------------------------------------*/
interchanges_ranked as (
    select  segment_id,
            interchange_id, 
            rank() over (
                partition by interchange_id 
                order by distance_km
            ) as ranked 
    from    distances 
),

/* ------------------------------------------------------------
   Select only the closest segment to each interchange.
-------------------------------------------------------------*/
closested_segment_to_interchange as (
    select  d.segment_id,
            d.interchange_id,
            d.distance_km
    from    interchanges_ranked ir
            join distances d 
                on d.segment_id = ir.segment_id 
                and d.interchange_id = ir.interchange_id 
    where   ranked = 1                
),

/* ------------------------------------------------------------
   Count how many interchanges are associated with each segment.
   Higher values may indicate more complex traffic conditions.
-------------------------------------------------------------*/
interchanges as ( 
    select  segment_id,
            count(distinct interchange_id) as interchange_rates
    from    closested_segment_to_interchange
    group   by segment_id
) 


/* ------------------------------------------------------------
   Final feature engineering step.
   Use NTILE(10) window functions to normalize each metric
   into a 1–10 ranking scale for scoring later in Python.
-------------------------------------------------------------*/
select  hwy.segment_id,
        aadt_total,
        aadt_ev,
        aadt_truck,
        peak_factor,
        interstate,
        lanes,
        speed_limit,
    
        /* High EV usage (more EV traffic is better) */
        ntile(10) over (
            order by ev_percentage desc
        ) as high_ev_vehicle_usage,
    
        /* Low truck usage (fewer trucks is better) */
        ntile(10) over (
            order by truck_percentage asc
        ) as low_truck_usage,
    
        /* Peak traffic factor (lower congestion preferred) */
        ntile(10) over (
            order by peak_factor desc
        ) as peak_time_bucket,
    
        /* Weather risk ranking (lower risk preferred) */
        ntile(10) over (
            order by risk_score asc
        ) as weather_risk_area,
    
        wetlands_nearby,
    
        /* Crash rate ranking */
        ntile(10) over (
            order by crash_rate asc
        ) as crash_rate,
    
        /* Incident rate ranking */
        ntile(10) over (
            order by incident_rate asc
        ) as incident_rate,
    
        /* Interchange density ranking */
        ntile(10) over (
            order by interchange_rates asc 
        ) as interchange_rates

from    highway_stats hwy 

        /* Attach wetland constraint counts */
        left outer join wetland_areas wet 
            on wet.segment_id = hwy.segment_id 
            
        /* Attach interchange proximity statistics */
        left outer join interchanges i 
            on i.segment_id = hwy.segment_id 