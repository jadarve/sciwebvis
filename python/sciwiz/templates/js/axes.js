

// TODO: get from Python
var axesProp = {
    width : {{prop['size'][0]}},
    height : {{prop['size'][1]}},
    bgcolor : 0xF0F0F0,
    color : new SCIWIZ.Color(0.9375, 0.9375, 0.9375)
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
