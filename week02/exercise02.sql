with stats as (
    select
        percentile_cont(0.25) within group (order by amount)as q1,
        percentile_cont(0.75) within group (order by amount) as q3
    from donations
),
bounds as (
    select
        q1,
        q3,
        (q3 - q1) as iqr,
        q1 - 1.5 * (q3 - q1) as lower_bound,
        q3 + 1.5 * (q3 - q1) as upper_bound
    from stats
)
select  
        -- Profile Check: some names seem to be formatted with a comma between last name and 
        --                  first name while others seem to have the name in order 
        contains(name, ',') as profile_name_format_invalid, 
        name,

        -- Profile Check: this checks to see if the birthdates are valid dates by using the s
        --                  snowflake function try_To_date which returns null if it is invalid  
        try_to_date(date_of_birth) is null as profile_dob_invalid, 
        date_of_birth,

        -- Profile Check: since all the birthdates seem invalid, this checks to see if the mm--dd
        --                  are at least valid dates; uses the leap year 2024 as a constant value 
        --                  (the actual month-day combinations do a seem always valid in this dataset)
        case when date_of_birth like '00%' then 
                    try_to_date(concat('2024-',substr(date_of_birth, 6))) is null
                else null end as profile_dob_mm_dd_invalid, 
        date_of_birth, 

        -- Profile Check: this is an established regex to test the validity of zip codes in the USA 
        not(regexp_like(zip, '(0[1-9]|[1-9]\\d)\\d{3}(-\\d{4})?')) as profile_zip_code_invalid, 
        zip, 

        -- Profile Check: this is an established regex to test the validity of phone number sin the USA 
        --                  since all the records had states associated with them, meaning that they are 
        --                  located in the USA; this does account for extension codes and a country code
        not(regexp_like(phone, '^(\\+?1[-.\\s]?)?(\\(\\d{3}\\)|\\d{3})[-.\\s]?\\d{3}[-.\\s]?\\d{4}(x\\d+)?$')) as profile_phone_format_invalid,
        phone, 
    
        -- Profile Check: just a null check for the category field 
        category is null as profile_category_null, 
        category,  

        -- Profile Check: a check for null/missing, unknown or N/A values in the category field to get a 
        --                  real idea on how much of this data is missing - is it essential? 
        category is null or category in ('N/A','Unknown') as profile_category_missing, 
        category, 

        -- Profile Check: this uses a known equation to check to make sure the donation amounts are within 
        --                  an appropriate, certain range and flags any rows that may be crazy amounts high   
        (amount < b.lower_bound OR amount > b.upper_bound) as profile_amount_invalid,
        amount 
        
from    data5035.spring26.donations as d 

        cross join bounds as b 

 
/*
Findings: 
- Donation_Id: Regular data, considered an ID therefore it doesn't need to increment normally but it seems to do this anyway. 
- Name: Formatted in two different ways with the "first_hame last_name" combination and then "last_name, first_name".  I did not 
    choose a correct way to format this but flagged if there was a comma present or not. 
- Age: There is no way to verify if this data is correct
- Date_Of_Birth: The year on these days is not normal.  Even if you try to guess at if it could be 1900's or 2000's leaves the
     Age field completely invalid.  Donation_id=2 has a Date_Of_Birth year of 01 and an Age of 28 but the data certainly didn't come 
     from 2027 since that is in the fuutre.  
- Street_Address: This data cannot be verified without running it through an address API of some kind 
- City: This data cannot be verified without running it through an address API of some kind
- State: Since the rest of the address data cannot be verified without outside resources, I left the State field alone 
- Zip: Some values have less than the standard 5 digits.  I used a known, established regex to test these values for USA zip codes. 
- Phone number: Sloppy input but mostly valid numbers.  I used a known, established regex to test these values for USA phone numbers. 
- Category: some data is null and missing entirely, some is just "Uknown" or "N/A" so I went through and flagged anything that was 
    not explicitly known because it seems like the field may not be in use all the time 
- Organization: This data is full of commas, hyphens, and abbreviations but it looks valid and distinct.  
- Amount: Some people donated crazy high amounts compared to the rest of the data.  I used a known, established equation/function to 
    find outliers in the data rather than just saying anything over $x is invalid.  
*/