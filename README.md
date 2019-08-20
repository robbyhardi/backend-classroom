# Google Classroom

A Python implementation of [Google Classroom](https://classroom.google.com/) using [Flask](http://flask.pocoo.org) as framework, [JSON](https://json.org) as data format and [Insomnia](https://insomnia.rest) as REST client.

## Installing
### Python
Install with pip:
```
pip install python
```
### Flask
Install with pip:
```
pip install flask
```
### Insomnia
Install Insomnia REST Client from https://insomnia.rest/

## Usage

### Create Class
Open Insomnia, create a request POST to `/class/create` with JSON body:

``` json
{
	"classname": "Javascript",
	"classid": 902,
	"teachers": [],
	"students": [],
	"classwork": [] 
}
```
### Register Students
Open Insomnia, create a request POST to `/register` with JSON body:

```json
{
  "classes_as_student": [],
  "classes_as_teacher": [],
  "email": "pram@gmail.com",
  "fullname": "Pram Makers",
  "password": "inipram",
  "userid": 19,
  "username": "Pramsi"
}
```

### Create Classworks
Open Insomnia, create a request POST to `/classwork/create` with JSON body:

```json
{
	"workid": 4,
	"class": 902,
	"question": "Apa guna if?" ,
	"answer": []
}
```

## Feature
### Basic
- [x] Register
- [x] Login
- [x] Create class
- [x] Get classlist
- [x] Update class
- [x] Delete class
- [x] Create classwork
- [x] Get classwork
- [x] Update classwork
- [x] Delete classwork
- [x] Asign classwork
- [x] Join class