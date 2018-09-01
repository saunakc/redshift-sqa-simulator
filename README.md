# redshift-sqa-simulator

This simulator creates 
--
  1. A AWS Lambda function in python that launches a SQL query stored in s3. Several queries can be stored in s3, among which only one will be launched randomly at a time.
  2. A AWS Step Function that executes the above AWS Lambda function in parallel.

Pre-requisites:
--

In order to execute the Lambda function you need a cluster created using the snapshot “rslab-ds2-xl-4n-final” from AWS account 413094830157. Please contact saunak@amazon.com, if you need a copy of the cluster snapshot with sample data.

Alternatively you can store your sample SQL queries in your own s3 bucket and update the cloudformation template with the s3 path.

Steps:
--

To start stack creation using CloudFormation template Click below:

[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=&templateURL=https://s3.amazonaws.com/awspsa-redshift-lab/cfn-templates-redshift-lab/StepFunctionLambda.yml)
 
* Click “Next” on the Select Template page.
* Enter "Stack name" example “StepFnLambda”. Leave everything else unchanged. Click “Next”. 
    Note: The stack name you enter will appear as prefix of the AWS Lambda function name, IAM role for Lambda and Step Function State             Machine that this template is going to create.
* Enter the Key = Owner and Value = Your_NAME. Expand Advanced and enable Termination Protection. Click “Next”.
* Check the "I acknowledge that AWS CloudFormation might create IAM resources." and click "Create".
* Monitor the progress of cluster launch from "Cloudformation" service navigation page. Successful completion of the stack will be marked with the status = “CREATE_COMPLETE”.
* At the end of successful execution of the stack four resources will get created which will be visible on Resources tab of the stack you just created. Click on the Physical ID of the resource of Type “AWS::StepFunctions::StateMachine”. The Physical ID will look something like “arn:aws:states:us-east-1:413094830157:stateMachine:LambdaStateMachine-BRcwDzke2wiW”.
* You are in Step Functions window in the AWS Console due to the click in previous step. Click on Edit. In the State machine definition window replace the JSON string definition by below text. REMEMBER to change the “Resources” value to the Lambda Function ARN created using the stack. Hit Save.
```json
{
  "Comment": "An example of the Amazon States Language using a parallel state to execute many branches of Lambda function at the same time.",
  "StartAt": "Parallel",
  "States": {
    "Parallel": {
      "Type": "Parallel",
      "Next": "Final State",
      "Branches": [
        {
          "StartAt": "RandomQuery1",
          "States": {
            "RandomQuery1": {
              "Type": "Task",
              "Resource": "arn:aws:lambda:us-east-1:413094830157:function:StepFnLambda-FunctionAMI-5NK6PI1EAGRH",
              "End": true
            }
          }
        },
        {
          "StartAt": "RandomQuery2",
          "States": {
            "RandomQuery2": {
              "Type": "Task",
              "Resource": "arn:aws:lambda:us-east-1:413094830157:function:StepFnLambda-FunctionAMI-5NK6PI1EAGRH",
              "End": true
            }
          }
        },
        {
          "StartAt": "RandomQuery3",
          "States": {
            "RandomQuery3": {
              "Type": "Task",
              "Resource": "arn:aws:lambda:us-east-1:413094830157:function:StepFnLambda-FunctionAMI-5NK6PI1EAGRH",
              "End": true
            }
          }
        },
        {
          "StartAt": "RandomQuery4",
          "States": {
            "RandomQuery4": {
              "Type": "Task",
              "Resource": "arn:aws:lambda:us-east-1:413094830157:function:StepFnLambda-FunctionAMI-5NK6PI1EAGRH",
              "End": true
            }
          }
        },
        {
          "StartAt": "RandomQuery5",
          "States": {
            "RandomQuery5": {
              "Type": "Task",
              "Resource": "arn:aws:lambda:us-east-1:413094830157:function:StepFnLambda-FunctionAMI-5NK6PI1EAGRH",
              "End": true
            }
          }
        },
        {
          "StartAt": "RandomQuery6",
          "States": {
            "RandomQuery6": {
              "Type": "Task",
              "Resource": "arn:aws:lambda:us-east-1:413094830157:function:StepFnLambda-FunctionAMI-5NK6PI1EAGRH",
              "End": true
            }
          }
        },
        {
          "StartAt": "RandomQuery7",
          "States": {
            "RandomQuery7": {
              "Type": "Task",
              "Resource": "arn:aws:lambda:us-east-1:413094830157:function:StepFnLambda-FunctionAMI-5NK6PI1EAGRH",
              "End": true
            }
          }
        },
        {
          "StartAt": "RandomQuery8",
          "States": {
            "RandomQuery8": {
              "Type": "Task",
              "Resource": "arn:aws:lambda:us-east-1:413094830157:function:StepFnLambda-FunctionAMI-5NK6PI1EAGRH",
              "End": true
            }
          }
        },
        {
          "StartAt": "RandomQuery9",
          "States": {
            "RandomQuery9": {
              "Type": "Task",
              "Resource": "arn:aws:lambda:us-east-1:413094830157:function:StepFnLambda-FunctionAMI-5NK6PI1EAGRH",
              "End": true
            }
          }
        },
        {
          "StartAt": "RandomQuery10",
          "States": {
            "RandomQuery10": {
              "Type": "Task",
              "Resource": "arn:aws:lambda:us-east-1:413094830157:function:StepFnLambda-FunctionAMI-5NK6PI1EAGRH",
              "End": true
            }
          }
        },
        {
          "StartAt": "Pass",
          "States": {
            "Pass": {
              "Type": "Pass",
              "Next": "Wait 10s"
            },
            "Wait 10s": {
              "Type": "Wait",
              "Seconds": 10,
              "End": true
            }
          }
        }
      ]
    },
    "Final State": {
      "Type": "Pass",
      "End": true
    }
  }
}
```
Resources:
--
Following resources will get created after the stack finished execution:
* AWS::Lambda::Function -> Python 2.7 code that connects to a Redshift cluster and launches a query.
* AWS::IAM::Role -> Attached policy AmazonS3ReadOnlyAccess for Lambda execution.
* AWS::StepFunctions::StateMachine -> State machine.
* AWS::IAM::Role -> Allow Lambda invoke.
 
Schedule the State Machine
--
The State Machine created by this template can be launched via Cloudwatch Events Rule.

1.	Log in into the AWS Console and navigate to service Cloudwatch.
2.	From the left navigation Click on Rules under Events. And then click on “Create rule”.
3.	Select “Schedule” as Event Source and make a selection for example 5 minutes.
4.	Click on Add Target > Step Functions state machine. Select the state machine that starts with "LambdaStateMachine-". Expand “**Configure input**” > **Constant (JSON text)**. In the text box enter below JSON-

**{"Host": "<Input_your_cluster_endpoint_name>",   "Port": 8192,   "Database": "awspsars",   "Password": "Welcome123",   "User": "labuser"}**
 
5.	Hit Configure details. 
6.	Provide Name as “labuser-<n>-lambdaQL” and make sure State is “Enabled”. Hit Create Rule.

