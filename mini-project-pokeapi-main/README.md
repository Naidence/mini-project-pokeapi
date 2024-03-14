# Pokemon Database using pokeapi

## Overview

Mini Projeng bootcam

The platform is written in Python using Flask (Backend), HTML CSS (Frontend) and MYSQL (Database).

## API Reference

#### Get Pokemon
Returns an specific Pokemon by either its national id or name

**GET** URL GLOBAL : pokeapi.co/api/v2/

Each Pokemon has the following fields:
- name
- id
- type
- base_stats
- description
- hp
- attack
- defense

#### Get national Pokeapi
Returns Pokeapi in JSON format.

**GET** pokeapi.co/api/v2/ 

#### Get regional Pokeapi
Returns the Pokemon Database of a all type 

**GET** {POKEMON_API_URL}/type?limit=10

Returns the Pokemon Database of a list by type 
**GET** {POKEMON_API_URL}/type/{type_name.lower()

Returns the detail of pokemon by name
**GET** https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}

## Notes

This is a work in progress. I will be adding new features to the API, and to the platform in general in the future. A development version is available SOON!.


## Project

This repository contains a single file (app.py) that has the web service code and the navigation of the application, several scripts used to transform the data, a template folder with the HTML code of the application,  and an export of the collection (pokemondataset.json).

## Hosting for Monitoring Tools (Zabbix) by GCP
url : http://34.87.102.193/zabbix/

## Hosting for pokemon database
url : SOON!