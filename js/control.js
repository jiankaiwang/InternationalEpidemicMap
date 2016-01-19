/*
 Control JS v1.0.0 (2016-1-8)

 (c) 2016 Center for Disease Control, Taiwan

 License: GNU GENERAL PUBLIC LICENSE
*/

// control color of each disease
function getAutoColor(getDisease) {
    switch (getDisease) {
        default:
            return "rgba(255,0,0,0.5)";
    }
}

// current zoom, min zoom (in) count, max zoom (out) count
var zoomState = [0, -5, 5];
// control zoom in and zoom out by count
function checkZoomState(getClickOption) {
    switch (getClickOption) {
        case 'in':
            if (zoomState[0] - 1 > zoomState[1]) {
                zoomState[0] = zoomState[0] - 1;
                return true;
            }
            return false;
        case 'out':
            if (zoomState[0] + 1 < zoomState[2]) {
                zoomState[0] = zoomState[0] + 1;
                return true;
            }
            return false;
    }
}

// v.1.0 select source based on the user selection
function searchStart() {
    var selectedSource = $("#search-select-source").val();;
    var selectedDate = $("#search-select-date").val();
    var selectedDisease = $("#search-select-disease").val();
    var autoColor = getAutoColor($("#search-select-disease").val());

    if (currentSelection != selectedSource + '_' + selectedDate + '_' + selectedDisease) {
        // save the current selection
        currentSelection = selectedSource + '_' + selectedDate + '_' + selectedDisease;

        // start to show the disease
        //var jsonUrl = '\\web\\highcharts\\world-health-map\\data\\dataJson\\' + selectedDate + '\\';
        var jsonUrl = 'data/dataJson/' + selectedDate + '/';
        jsonUrl += selectedSource + '_' + selectedDate + '_' + selectedDisease + ".json";
        getJSONMap(selectedDisease, jsonUrl, autoColor);
    }
}


// selection panel
var hash2Value = {};
var getCurrentId = '';
var currentIndex = '';

function appendItem(getInitialValue) {
    // total append data
    var ttlAppendData = '';
    for (var hashName in hash2Value) {
        if (hash2Value.hasOwnProperty(hashName)) {
            if (hashName == getInitialValue) {
                if (hashName == "summary") {
                    ttlAppendData = '<option value="' + hashName + '" selected>' + hash2Value[hashName] + '</option>' + ttlAppendData;
                } else {
                    //$("#" + getCurrentId).append('<option value="' + hashName + '" selected>' + hash2Value[hashName] + '</option>');
                    ttlAppendData = ttlAppendData + '<option value="' + hashName + '" selected>' + hash2Value[hashName] + '</option>';
                }
            } else {
                //$("#" + getCurrentId).append('<option value="' + hashName + '">' + hash2Value[hashName] + '</option>');
                ttlAppendData = ttlAppendData + '<option value="' + hashName + '">' + hash2Value[hashName] + '</option>';
            }
        }
    }
    $("#" + getCurrentId).append(ttlAppendData);

    // initialization
    hash2Value = {};
}

function clickToShowDisList(getDateJson, getOption) {
    // delete options
    $("#search-select-disease option").remove();

    // add options
    //$.getJSON("\\web\\highcharts\\world-health-map\\data\\selJson\\cdctw_" + getDateJson + "_selection.json", function(data) {
    $.getJSON("data/selJson/cdctw_" + getDateJson + "_selection.json", function (data) {
        for (var index in data) {
            // initial 
            if (currentIndex == '') {
                currentIndex = index;
            } else {
                // start to append
                appendItem("summary");

                // set for next id
                currentIndex = index;
            }

            for (var hashIndex in data[index]) {
                switch (hashIndex) {
                    case "id":
                        getCurrentId = (data[index])[hashIndex];
                        break;
                    default:
                        hash2Value[hashIndex] = (data[index])[hashIndex];
                        break;
                }
            }
        }

        // finish the last selection
        appendItem("summary");

        // start to show the disease
        if (getOption == 1) {
            searchStart();
        }
    });
}

// control expension
var currentState = 1;
var currentInforState = 1;
function ctlExpension(getObjectOption, getTime) {
    switch (getObjectOption) {
        case 'search-source-class':
            if (currentState == 1) {
                $(".search-source-class").hide(getTime);
                currentState = 0;
            } else {
                $(".search-source-class").show(getTime);
                currentState = 1;
            }
            break;
        case 'inforTab':
            if (currentInforState == 1) {
                $("#inforTab").hide(getTime);
                $("#inforTab").css({ "border": "none" });
                currentInforState = 0;
            } else {
                $("#inforTab").show(getTime);
                $("#inforTab").css({ "border": "1px solid rgba(27,141,61,1)" });
                currentInforState = 1;
            }
            break;
    }
}

// get geo location and ROC as default location
var cntLocation = { "color": "rgba(10,10,10,1)", "Country": "R.O.C. (中華民國)", "code": "TW", "z": 5, "description": "目前位置" };
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(

		// get geo location
		function (position) {
		    // google map geocoder setting
		    var geocoder = new google.maps.Geocoder();
		    var latitude = position.coords.latitude;
		    var longitude = position.coords.longitude;
		    var latlong = new google.maps.LatLng(latitude, longitude);
		    var accuracy = position.coords.accuracy;

		    // start to use decoder
		    geocoder.geocode({ 'latLng': latlong }, function (results, status) {
		        if (status == google.maps.GeocoderStatus.OK) {
		            if (results[0]) {

		                // get country name
		                for (var i = 0; i < results[0].address_components.length; i++) {
		                    var shortname = results[0].address_components[i].short_name;
		                    var longname = results[0].address_components[i].long_name;
		                    var allType = results[0].address_components[i].types;

		                    // the country in the list
		                    if (allType.indexOf("country") != -1) {
		                        if (!isNullOrWhitespace(shortname)) {
		                            startToAddNearInfo(1, shortname);
		                            //startToAddNearInfo(1,"US");
		                        }
		                        else {
		                            region = longname;
		                        }
		                    }
		                }
		            }
		        }
		    });
		},
		// does not allow geo location
		function error(msg) {
		    $("#infor-body-title-body").text("無法定位現在位置，使用預設位置 TW");
		    startToAddNearInfo(0, "");
		}, {
		    maximumAge: 600000, timeout: 5000, enableHighAccuracy: true
		});

    } else {
        $("#infor-body-title-body").text("瀏覽器並不支援定位，使用預設位置 TW");
        startToAddNearInfo(0, "");
    }
}

function startToAddNearInfo(getOption, getCountryName) {
    switch (getOption) {
        case 0:
            // (1) browser can not support, (2) user does not allow to share its position
            // work as the default
            currentCode[1] = "TW";
            break;
        case 1:
            // use the short name to show the country code (iso-a2)
            $("#infor-body-title-body").text("目前位置: " + getCountryName);
            currentCode[1] = getCountryName;
            break;
    }

    // start to find near by countries
    startToFindRegion();

    // start to find the near by country, but only the initialization
    appendInterEpiInfo();
}

// regular expression
function isNullOrWhitespace(text) {
    if (text == null) {
        return true;
    }
    return text.replace(/\s/gi, '').length < 1;
}


// ttlRegionList :  region name => [country 1, country 2, ...]
var ttlRegionList = {};
var currentCode = ["", ""];
var tmpList = ['', ''];

function startToFindRegion() {
    for (i = 0; i < (Highcharts.maps["custom/world"]["features"]).length ; i++) {
        // complete the ttlRegionList, region -> country code
        tmpList[0] = Highcharts.maps["custom/world"]["features"][i]["properties"]["region-wb"];
        tmpList[1] = Highcharts.maps["custom/world"]["features"][i]["properties"]["iso-a2"];
        if (ttlRegionList.hasOwnProperty(tmpList[0])) {
            ttlRegionList[tmpList[0]].push(tmpList[1]);
        } else {
            ttlRegionList[tmpList[0]] = [tmpList[1]];
        }

        // find the same region of current country code
        if (currentCode[1] == tmpList[1]) {
            currentCode[0] = tmpList[0];
        }
    }
}

// start to find the near by countries and append the international epidemic information
// only the first time to load the near by countries
var initialLoadOrNot = 0;
function appendInterEpiInfo() {
    if (initialLoadOrNot != 0) {
        // already done
        return;
    }
    initialLoadOrNot = 1;
    for (i = 0; i < getJsonFromSummary.length; i++) {
        if (ttlRegionList[currentCode[0]].indexOf(getJsonFromSummary[i]["code"]) > -1) {
            // start to append
            appendStr = '<ul class="infor-body-list">';
            appendStr = appendStr + '<li class="infor-body-list-item">' + getJsonFromSummary[i]["Country"] + '</li>';
            appendStr = appendStr + '<li class="infor-body-list-item-2">' + getJsonFromSummary[i]["description"] + '</li>';
            appendStr = appendStr + '</ul><hr class="infor-body-list-hr"></hr>';
            $("#inforTab-disease").append(appendStr);
        }
    }
}






