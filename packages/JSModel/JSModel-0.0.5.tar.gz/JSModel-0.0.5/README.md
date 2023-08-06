# JsonModel Guide

JSModel Package is a python package that helps to work with Json Data more efficiently

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install **JsonModel**.

```bash
pip install JSModel
```


## Usage

```python
from JSModel import ParseModel

data = {
    "A": "This is A",
    "B": "This is B",
    "C": "This is C",
}


### Create your Model ###
class ModelA:
    ThisA = "A"
    ThisB = "B"
    ThisC = "C"
    ThisD = "D"


parse_model = ParseModel(ModelA)
parse_model.data(data)
result = parse_model.parse(null_value=None,
                           error_if_null=False
                           )
print(result)
### output: {'ThisA': 'This is A', 'ThisB': 'This is B', 'ThisC': 'This is C', 'ThisD': 'None'}

## if error_if_null =True --> This will raise error if the key is not found
result = parse_model.parse(null_value=None,
                           error_if_null=True
                           )
### output: KeyError: 'D'

### null_value is to assigned a default value if the key is not found
result = parse_model.parse(
    null_value="This is Empty",
    error_if_null=False
    )
print(result)


### output: {'ThisA': 'This is A', 'ThisB': 'This is B', 'ThisC': 'This is C', 'ThisD': 'This is Empty'}

### It can also Accept a Json Array data as well as List within the model.
class A:
    valueA = ["Data", "Information", "Age"]


data = [
    {
        "Data": {
            "Information":
                {
                    "Age": "20"
                }
        },
    },
    {
        "Data": {
            "Information":
                {
                    "Age": "22"
                }
        },
    }
    instance = ParseModel(A)
instance.data(data)
return_data = instance.parse()
## return_data is a Iterator Type


## output:
{'valueA': '20'}
{'valueA': '22'}
```

## Complex Model:

```python
from JSModel import ParseModel
from Utilities import credential_data
from JSModel import SubModel


class delivery_type_model(SubModel):
    target_node = "ceterms:targetNode"
    target_node_name = "ceterms:targetNodeName"


class Courses:
    type = "@type"
    ctid = "ceterms:ctid"
    name = "ceterms:name"
    keyword = ["ceterms:keyword", "en-US"]
    ownedby = "ceterms:ownedBy"
    offeredBy = "ceterms:offeredBy"
    description = "ceterms:description"
    delivery_type = delivery_type_model(
        "ceterms:deliveryType"
        )
    dateEffective = "ceterms:dateEffective"
    subject_webpage = "ceterms:subjectWebpage"
    availableOnlineAt = "ceterms:availableOnlineAt"
    version = "ceterms:versionIdentifier"
    learning_method = "ceterms:learningMethodType"
    life_cycle_status = "ceterms:lifeCycleStatusType"


ctid = ["ce-55873e03-f228-4ed2-81ee-7179b7636c27",
        "ce-d981d38d-8087-4272-bf44-b6d8ac6abd68"]
instance = credential_data.ctids(ctid)

Courses_Model = ParseModel(Courses)
"""
The data is attracted from public data from https://credentialengine.org
Here are the full link
"https://credentialengineregistry.org/resources/ce-55873e03-f228-4ed2-81ee-7179b7636c27"

"https://credentialengineregistry.org/resources/ce-d981d38d-8087-4272-bf44-b6d8ac6abd68"


"""
```
```json
{
   "@context":"https://credreg.net/ctdl/schema/context/json",
   "@id":"https://credentialengineregistry.org/resources/ce-55873e03-f228-4ed2-81ee-7179b7636c27",
   "@type":"ceterms:Course",
   "ceterms:ctid":"ce-55873e03-f228-4ed2-81ee-7179b7636c27",
   "ceterms:name":{
      "en-US":"Automotive Electrical Fundamentals and Applications"
   },
   "ceterms:keyword":{
      "en-US":[
         "Cohort 1",
         "Cohort 2"
      ]
   },
   "ceterms:ownedBy":[
      "https://credentialengineregistry.org/resources/ce-985b6759-2efc-4062-81a7-66a9dbdf394a"
   ],
   "ceterms:offeredBy":[
      "https://credentialengineregistry.org/resources/ce-985b6759-2efc-4062-81a7-66a9dbdf394a"
   ],
   "ceterms:inLanguage":[
      "en"
   ],
   "ceterms:description":{
      "en-US":"Automotive Electrical Fundamentals and Applications - UAUT 128"
   },
   "ceterms:deliveryType":[
      {
         "@type":"ceterms:CredentialAlignmentObject",
         "ceterms:framework":"https://credreg.net/ctdl/terms/Delivery",
         "ceterms:targetNode":"deliveryType:InPerson",
         "ceterms:frameworkName":{
            "en-US":"Delivery Type"
         },
         "ceterms:targetNodeName":{
            "en-US":"In-Person Only"
         },
         "ceterms:targetNodeDescription":{
            "en-US":"Delivery is only face-to-face."
         }
      }
   ],
   "ceterms:dateEffective":"2021-10-04",
   "ceterms:subjectWebpage":"https://go.pima.edu/automotive-technology",
   "ceterms:availableOnlineAt":[
      "https://go.pima.edu/automotive-technology"
   ],
   "ceterms:versionIdentifier":[
      {
         "@type":"ceterms:IdentifierValue",
         "ceterms:identifierValueCode":"UAUT 128"
      }
   ],
   "ceterms:learningMethodType":[
      {
         "@type":"ceterms:CredentialAlignmentObject",
         "ceterms:framework":"https://credreg.net/ctdl/terms/LearningMethod",
         "ceterms:targetNode":"learnMethod:Lecture",
         "ceterms:frameworkName":{
            "en-US":"Learning Method"
         },
         "ceterms:targetNodeName":{
            "en-US":"Lecture"
         },
         "ceterms:targetNodeDescription":{
            "en-US":"Primary method is presentation by an instructor of learning material and may include student discussion."
         }
      }
   ],
   "ceterms:lifeCycleStatusType":{
      "@type":"ceterms:CredentialAlignmentObject",
      "ceterms:framework":"https://credreg.net/ctdl/terms/LifeCycleStatus",
      "ceterms:targetNode":"lifeCycle:Active",
      "ceterms:frameworkName":{
         "en-US":"Life Cycle Status"
      },
      "ceterms:targetNodeName":{
         "en-US":"Active"
      },
      "ceterms:targetNodeDescription":{
         "en-US":"Resource is active, current, ongoing, offered, operational, or available."
      }
   }
}
```
```python


for data in instance:
    Courses_Model.data(data)
    # result=Courses_Model.parse(error_if_null=False)
    # for i in result:
    #     print(i)
    for i in Courses_Model.parse():
        print(i)
```
### Output: 
```json
{
   "availableOnlineAt":[
      "https://go.pima.edu/automotive-technology"
   ],
   "ctid":"ce-55873e03-f228-4ed2-81ee-7179b7636c27",
   "dateEffective":"2021-10-04",
   "delivery_type":[
      {
         "target_node":"deliveryType:InPerson",
         "target_node_name":{
            "en-US":"In-Person Only"
         }
      }
   ],
   "description":{
      "en-US":"Automotive Electrical Fundamentals and Applications - UAUT 128"
   },
   "keyword":[
      "Cohort 1",
      "Cohort 2"
   ],
   "learning_method":[
      {
         "@type":"ceterms:CredentialAlignmentObject",
         "ceterms:framework":"https://credreg.net/ctdl/terms/LearningMethod",
         "ceterms:targetNode":"learnMethod:Lecture",
         "ceterms:frameworkName":{
            "en-US":"Learning Method"
         },
         "ceterms:targetNodeName":{
            "en-US":"Lecture"
         },
         "ceterms:targetNodeDescription":{
            "en-US":"Primary method is presentation by an instructor of learning material and may include student discussion."
         }
      }
   ],
   "life_cycle_status":{
      "@type":"ceterms:CredentialAlignmentObject",
      "ceterms:framework":"https://credreg.net/ctdl/terms/LifeCycleStatus",
      "ceterms:targetNode":"lifeCycle:Active",
      "ceterms:frameworkName":{
         "en-US":"Life Cycle Status"
      },
      "ceterms:targetNodeName":{
         "en-US":"Active"
      },
      "ceterms:targetNodeDescription":{
         "en-US":"Resource is active, current, ongoing, offered, operational, or available."
      }
   },
   "name":{
      "en-US":"Automotive Electrical Fundamentals and Applications"
   },
   "offeredBy":[
      "https://credentialengineregistry.org/resources/ce-985b6759-2efc-4062-81a7-66a9dbdf394a"
   ],
   "ownedby":[
      "https://credentialengineregistry.org/resources/ce-985b6759-2efc-4062-81a7-66a9dbdf394a"
   ],
   "subject_webpage":"https://go.pima.edu/automotive-technology",
   "type":"ceterms:Course",
   "version":[
      {
         "@type":"ceterms:IdentifierValue",
         "ceterms:identifierValueCode":"UAUT 128"
      }
   ]
}
```
```json
{
   "availableOnlineAt":"None",
   "ctid":"ce-d981d38d-8087-4272-bf44-b6d8ac6abd68",
   "dateEffective":"None",
   "delivery_type":"None",
   "description":{
      "en-US":"Study of current office procedures, duties, and responsibilities applicable to an office environment. The series includes instruction in word processing, spreadsheet, databases, presentation software, Internet searching, as well as data entry, practical business applications, business math and business communications"
   },
   "keyword":"None",
   "learning_method":"None",
   "life_cycle_status":{
      "@type":"ceterms:CredentialAlignmentObject",
      "ceterms:framework":"https://credreg.net/ctdl/terms/LifeCycleStatus",
      "ceterms:targetNode":"lifeCycle:Active",
      "ceterms:frameworkName":{
         "en-US":"Life Cycle Status"
      },
      "ceterms:targetNodeName":{
         "en-US":"Active"
      },
      "ceterms:targetNodeDescription":{
         "en-US":"Resource is active, current, ongoing, offered, operational, or available."
      }
   },
   "name":{
      "en-US":"Administrative Assistant Series"
   },
   "offeredBy":"None",
   "ownedby":[
      "https://credentialengineregistry.org/resources/ce-392226c8-d9ee-4680-9a52-a4f8707dbf5f"
   ],
   "subject_webpage":"https://sites.austincc.edu/admin-ce/poft-1070-administrative-assistant-series",
   "type":"ceterms:Course",
   "version":"None"
}
```



## License
[MIT](https://choosealicense.com/licenses/mit/)