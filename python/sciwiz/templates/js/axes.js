

// TODO: get from Python
var axesProp = {
    width : 800,
    height : 800,
    bgcolor : 0x707070
};

var axes = fig.addAxes(axesProp);


// Render objects
{% for obj in objects %}
///////////////////////////////////////
{
{{obj}}
};
///////////////////////////////////////
{% endfor %}


// re-render
axes.needsUpdate = true;
axes.render();
axes.render();
