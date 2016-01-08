
var materialDict = new Array();

initMaterials();

function initMaterials() {

    // each material is an instance of SCIWIS.Material class
    {% for mat in materials.viewitems() %}
    materialDict['{{mat[0]}}'] = new {{mat[1]}};{% endfor %}
}