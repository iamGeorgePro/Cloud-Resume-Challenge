import boto3
import os
import json

def lambda_handler(event: any, context: any):

    try:
        users: str = event["users"]
        visit_count: int = 0

        #create a dynamodb resource
        dynamodb = boto3.resource('dynamodb')
        table_name = os.environ["TABLE_NAME"]
        table_name = "user-count"
        table = dynamodb.Table(table_name)

        "Get the current visit count from the database"
        response = table.get_item(Key={'users': 'users'})
        if "Item" in response:
            visit_count = response["Item"]["visit_count"]

        #"Increment the visit count"
        visit_count += 1

        #Update the database with the new visit count
        table.put_item(
            Item={'users': 'users', 
            "visit_count": visit_count
                }
        )

        message: str = f"Hello {'users'}! You have visited {visit_count} times."
        return {
             'statusCode': 200,
             'headers': {'Content-Type': 'application/json'},
             'body': json.dumps({"mess": message})}
    except Exception as e:
        return {
             'statusCode': 500,
             'headers': {'Content-Type': 'application/json'},
             'body': json.dumps({"error": str(e)})}


if __name__ == "__main__":
    os.environ["TABLE_NAME"] = "visit-count-table"
    test_event = {"users": "George"}
    result = lambda_handler(test_event, None)
    print(result)
    