// data, geometries and materials
var dataDict = new Array();
var geometryDict = new Array();
var materialDict = new Array();

//#####################################
// FIGURE
//#####################################
var figProp = {ID: '{{ID}}'};
var fig = new SCIWIS.Figure(figProp);


//#####################################
// DATA
//#####################################
try {
    {% for item in DATA.viewitems() %}
    dataDict['{{item[0]}}'] = NJ.fromJson('{{item[1]}}');{% endfor %}
} catch(e) {
    console.log('error parsing NUMJIS JSON: ' + e.message);
}

//#####################################
// GEOMETRY
//#####################################
{% for g in GEOMETRY.viewitems() %}
geometryDict['{{g[0]}}'] = new {{g[1]}};{% endfor %}

//#####################################
// MATERIALS
//#####################################
{% for mat in MATERIALS.viewitems() %}
materialDict['{{mat[0]}}'] = new {{mat[1]}};{% endfor %}

//#####################################
// AXES
//#####################################
{% for ax in AXES %}
{{ax}} {% endfor%}


console.log('figure creation completed');