import json


def lambda_handler(event, context):
    if event["queryStringParameters"] is None:
        return {
            'statusCode': 200,
            'body': json.dumps('var1 ve var2 degerini tanimlayin')
        }

    var1_not_found = "var1 degerini tanimlayin!"
    var1 = event["queryStringParameters"].get('var1', var1_not_found)

    if var1 == var1_not_found:
        return {
            'statusCode': 200,
            'body': json.dumps(var1_not_found)
        }

    var2_not_found = "var2 degerini tanimlayin!"
    var2 = event["queryStringParameters"].get('var2', var2_not_found)

    if var2 == var2_not_found:
        return {
            'statusCode': 200,
            'body': json.dumps(var2_not_found)
        }

    var1 = int(event["queryStringParameters"]['var1'])
    var2 = int(event["queryStringParameters"]['var2'])
    total = var1 + var2

    return {
        'statusCode': 200,
        'body': json.dumps(total)
    }