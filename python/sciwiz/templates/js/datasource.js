
var dataDict = new Array();

initData();

function initData() {

    // create NUMJIS arrays from JSON code
    try {
    {% for item in DATA.viewitems() %}
        dataDict['{{item[0]}}'] = NJ.fromJson('{{item[1]}}');
    {% endfor %}
    } catch(e) {
        console.log('error parsing NUMJIS JSON: ' + e.message);
    }
}

// below goes the code creating the renderer