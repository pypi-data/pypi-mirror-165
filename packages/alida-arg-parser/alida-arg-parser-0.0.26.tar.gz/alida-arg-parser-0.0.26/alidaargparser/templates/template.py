{
    "name": "{{ name }}",
    "description": "{{ description }}",
    "mode": "{{mode.upper()}}",
    "area": "{{area.upper()}}",
    "url":  {{json.dumps(docker_image)}},
    "version": "1.0.0",
    "framework": {
        "id": 6,
        "name": "Python",
        "version": "3",
        "imageUrl": "https://cdn.alidalab.it/static/images/frameworks/python_logo.png"
    },
    "properties": [
        {% for input_dataset in input_datasets %}
        {
            "description": {{json.dumps(input_dataset.description)}},
            "mandatory": true,
            "type": "application",
            "defaultValue": null,
            "value": null,
            "key": "input-dataset",
            "valueType": "STRING",
            "inputData": null,
            "outputData": null
        },
		{
			"defaultValue": {{json.dumps(translation['column_types'][input_dataset.columns_type])}},
			"description": "Selected columns from table",
			"key": "input-columns",
			"type": "application",
			"mandatory": true,
			"valueType": "STRING",
			"value": null,
			"inputData": null,
			"outputData": null
		},
        {% endfor %}
        {% for output_dataset in output_datasets %}
        {
            "description": {{json.dumps(output_dataset.description)}},
            "mandatory": true,
            "type": "application",
            "defaultValue": null,
            "value": null,
            "key": "output-dataset",
            "valueType": "STRING",
            "inputData": null,
            "outputData": null
        },
        {% endfor %}
        {% for input_model in input_models %}
        {   
            "description": {{json.dumps(input_model.description)}},
            "mandatory": true,
            "type": "application",
            "defaultValue": null,
            "value": null,
            "key": "input-model",
            "valueType": "STRING",
            "inputData": null,
            "outputData": null
        },
        {% endfor %}
        {% for output_model in output_models %}
        {   
            "description": {{json.dumps(output_model.description)}},
            "mandatory": true,
            "type": "application",
            "defaultValue": null,
            "value": null,
            "key": "output-model",
            "valueType": "STRING",
            "inputData": null,
            "outputData": null
        },
        {% endfor %}
        {% for property in properties %}
        {
            "description": {{json.dumps(property.description)}},
            "mandatory": {{json.dumps(property.required)}},
            "type": "application",
            "defaultValue": {{json.dumps(property.default)}},
            "value": null,
            "key": {{json.dumps(property.name)}},
            "valueType": {{json.dumps(translation['type'][property.type])}},
            "inputData": null,
            "outputData": null
        },
        {% endfor %}
    ],
    "metrics": []
}

