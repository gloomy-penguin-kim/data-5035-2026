/******************************************************************************
Deliverable #1 
Kimball-Style Bus Matrix
*******************************************************************************/
/*  Kimball-Style Bus Matrix 
Business Process            Product     Formulation     Batch       Material        Supplier    Facility    Metrics
----------------            -------     -----------     -----       --------        --------    --------    -------
Batch Production            X           X               X                                       X           planned/actual/good/rejected quantities
Material Consumption        X                           X           X                                       quantity used
Material Receiving                                                  X               X                       quantity received
Quality Testing             X                           X                                                   pass/fail flag
Forumlation Definition      X           X                                                                   target batch size 
*/


use database USER$DOLPHIN; 

/******************************************************************************
Deliverable #2
Star Schema
*******************************************************************************/

create or replace temporary table facility (
    facility_id number autoincrement start 1 increment 1 primary key, 
    facility_name varchar(255)
);

create or replace temporary table facility_line (
    facility_line_id number autoincrement start 1 increment 1 primary key,
    facility_id number references facility(facility_id), 
    facility_line_name varchar(255)
);

create or replace temporary table employee_shift (
    employee_shift_id number autoincrement start 1 increment 1 primary key, 
    employee_shift_title varchar(255),
    employee_shift_wage number(10,2),
    employee_shift_shift int,  
    facility_line_id number references facility_line(facility_line_id)
);

create or replace temporary table employee_role (
    employee_role_id number autoincrement start 1 increment 1 primary key, 
    employee_role_title varchar(255),
    employee_role_description varchar(255) 
);

create or replace temporary table employee (
    employee_id number autoincrement start 1 increment 1 primary key, 
    employee_name varchar(255),
    employee_role_id number references employee_role(employee_role_id)
); 

create or replace temporary table employee_shift_assignment (
    employee_shift_assignment_id number autoincrement start 1 increment 1 primary key,
    employee_id number references employee(employee_id),
    employee_shift_id number references employee_shift(employee_shift_id),
    employee_shift_assignment_start_date timestamp, 
    employee_shift_assignment_end_date timestamp
);

create or replace temporary table brand (
    brand_id number autoincrement start 1 increment 1 primary key,
    brand_name varchar(255)
); 

create or replace temporary table material (
    material_id number autoincrement start 1 increment 1 primary key,
    material_name varchar(255),
    brand_id number references brand(brand_id),
    material_amount int 
);  

create or replace temporary table material_cost (
    material_cost_id number autoincrement start 1 increment 1 primary key,
    facility_id number references facility(facility_id), 
    material_id number references material(material_id),
    material_cost_price number(10,2) 
);

create or replace temporary table batch_status ( 
    batch_status_id number autoincrement start 1 increment 1 primary key,
    batch_status_name varchar(255)
);

create or replace temporary table batch (
    batch_id number autoincrement start 1 increment 1 primary key,  
    facility_line_id number references facility_line(facility_line_id),
    material_id number references material(material_id), 
    projected_quantity int, 
    actual_quantity int,
    batch_status number references batch_status(batch_status_id),
    batch_start_date timestamp, 
    batch_end_date timestamp 
);

create or replace temporary table quality_test_failure_type ( 
    quality_test_failure_type_id number autoincrement start 1 increment 1 primary key, 
    quality_test_failure_type_desc varchar(255), 
    quality_test_failure_type_cost decimal(10,2)
);

create or replace temporary table quality_test_type ( 
    quality_test_type_id number autoincrement start 1 increment 1 primary key, 
    quality_test_type_desc varchar(255)
);

create or replace temporary table quality_test ( 
    quality_test_id number autoincrement start 1 increment 1 primary key, 
    quality_test_desc varchar(255),  
    quality_test_cost decimal(10,2),
    quality_test_type_id number references quality_test_type(quality_test_type_id) 
);
 
create or replace temporary table dim_date ( 
    date_id number autoincrement start 1 increment 1 primary key, 
    date date,
    year number, 
    month number, 
    day number,
    day_of_week number,
    week_of_year number, 
    fiscal_year number 
);

create or replace temporary table batch_quality_test (
    batch_quality_test_id number autoincrement start 1 increment 1 primary key,  
    quality_test_id number references quality_test(quality_test_id),  
    batch_id number references batch(batch_id), 
    quality_test_result varchar(255), 
    quality_test_failure_type_id number references quality_test_failure_type(quality_test_failure_type_id),
    date_id number references dim_date(date_id), 
    batch_quality_test_timestamp timestamp
);




/******************************************************************************
Deliverable #3 
Reverse ETL Table 
*******************************************************************************/

create or replace temporary table cost_alert (
    cost_alert_id number autoincrement start 1 increment 1 primary key,
    
    facility_id number references facility(facility_id),
    batch_id number references batch(batch_id),
    
    alert_type varchar(255),           
    alert_severity varchar(50),        
    
    alert_message varchar(500),
    
    alert_payload variant,             
    
    created_at timestamp default current_timestamp()
);

/*
Example alert_payload JSON:

{
  "alert_category": "COST_OVERRUN",
  "description": "overhead and quality assurance",

  "batch": {
    "batch_id": "B-10454",
    "facility": "Columbus",
    "facility_type": "ISO 5 Cleanroom"
  },

  "production": {
    "standard_hours": 12.0,
    "actual_hours": 13.5,
    "overrun_hours": 1.5,
    "hourly_overhead_rate": 320.00,
    "expected_overhead_cost": 3840.00,
    "actual_overhead_cost": 4320.00,
    "overhead_variance": 400.00 
  },

  "facility_rates": {
    "columbus": 320.00,
    "st_louis": 180.00,
    "raleigh": 210.00
  },
 
  "hold_days": 9,
  "daily_cost": 150.00, 

  "total_cost_impact": {
    "overhead_overrun": 480.00,
    "qa_hold_cost": 1350.00,
    "total_extra_cost": 1830.00
  },

  "thresholds": {
    "max_allowed_hours_variance_pct": 10,
    "max_allowed_hold_days": 2
  },

  "trigger_reason": [
    "Production time exceeded standard by 12.5%",
    "QA hold exceeded threshold (9 days > 2 days)"
  ],

  "timestamp": "YYYY-MM-DDThh:mm:ssZ"
}
*/