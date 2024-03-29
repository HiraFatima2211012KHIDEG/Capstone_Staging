# Capstone Staging
### Check the presence of people more than expected, and owner will take security precautions accordingly
## DEG Group 2 (D. Battalion)

## Group Members

| Name | Roll Number | Email |
| ----- | ----- | ----- |
| Zubair Khatti | 2211-035-KHI-DEG | zubair.khatti@xloopdigital.com | 
| Syed Muhammad Mehmaam | 2211-028-KHI-DEG| syed.mehmaam@xloopdigital.com|
| Syeda Sayam Fatima Naqvi | 2211-031-KHI-DEG | sayam.fatima@xloopdigital.com|
| Hira Fatima | 2211-012-KHI-DEG | hira.fatima@xloopdigital.com |
| Muhammad Humza | 2211-018-KHI-DEG | mohammad.humza@xloopdigital.com |
| Muhammad Adnan Khalid | 2211-014-KHI-DEG| mohammad.adnan@xloopdigital.com|
| Anoosha Malik | 2211-004-KHI-DEG  | anoosha.malik@xloopdigital.com |

## Contributing Sections

### Conventions

| Name | Conventions |
| ----- | ----- |
| Branch Name | firstname-feature |
| Floder Name | snake_case |
| File Name | snake_case |
| Class Name | PascalCase |
| Function Name | snake_case |
| Variable Name | snake_case |

# About sensorsmock serivce
for successful run, first edit `docker-compose.yml` file
to know your aws session token, run this command in terminal:
~~~
aws sts get-session-token --duration-seconds 129600
~~~
then, edit `docker-compose.yml` file as described:
~~~
environment:
      - SMART_THERMO_BUCKET=<your-s3-bucket-name>
      - CARBON_SENSE_URL=http://extract_service:4008/collect_carbon_sense
      - MOISTURE_MATE_URL=http://extract_service:4008/collect_moisture_mate
      - AWS_ACCESS_KEY_ID=<your-access-key-id>
      - AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
      - AWS_SESSION_TOKEN=<your-session-token>
~~~
after setup your session token, run:
~~~
docker compose up
~~~
## Running the Application

To start the application, run the start.sh shell script:
~~~
sh initialize.sh
~~~

This will start the Kafka broker service, wait for 20 seconds, and then start the other services.