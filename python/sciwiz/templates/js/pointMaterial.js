
// create a SCIWIZ.PointMaterial object
var matprop = {
    {% for item in properties %}
    item[0] : item[1],
    {% endfor %}
};

var mat = new SCIWIZ.PointMaterial(matprop)