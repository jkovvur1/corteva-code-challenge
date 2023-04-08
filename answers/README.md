# Corteva Code challenge answers
### Instructions to setup and run the code

## Assumptions
- POSTGRESql is installed and running on your local or at remote

## Problem 1
- Create a Database weatherdb in POSTGRES and create the tables mentioned in `problem1.sql`

## Problem 2
- Install requirements in  `requirements.txt`
- Changer username, password, host etc required settings in `problem2.py` to connect to the POSTGRES instance
- Run problem2.py using
  ``` 
    python3 problem2.py 
  ```
 ## Problem 3
 - run the first query in `problem3.sql` in POSTGRES to create relation to store the computed values
 - run the second query to compute the averages and store them in the table created above

## Problem 4
- As we have already installed the required packagaes above. we are not required to run it again.
- Changer username, password, host etc required settings in `main.py` to connect to the POSTGRES instance
- run the code using
    ```
    uvicorn main:app --host '0.0.0.0' --port 8000
    ```
 - You can access the API Swagger page on `http://localhost:8000/docs`
 
## Extra Credit - Deployment
- Please go through the `deployment-ideas.txt` file for this

:v: