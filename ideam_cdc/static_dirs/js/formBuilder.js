/* Custom Form Builder
 * Author:Manre
 * Author e-mail:nobmann88@gmail.com
 * Version:0.1
 * Created:October 2016
 * File Description: This class will modify the page to create a custom form
 */

$(document).ready(function () {

    var map;

    function init_osm() {
        var mymap = L.map('map').setView([4.6870819, -74.0808636], 5);

        L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpandmbXliNDBjZWd2M2x6bDk3c2ZtOTkifQ._QA7i5Mpkd_m30IGElHziw', {
            maxZoom: 15,
            attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
            '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
            'Imagery © <a href="http://mapbox.com">Mapbox</a>',
            id: 'mapbox.streets'
        }).addTo(mymap);

        var areaSelect = L.areaSelect({width: 200, height: 250});
        areaSelect.on("change", function () {
            var bounds = this.getBounds();
            document.getElementById("sw_latitude").value = Math.ceil(bounds.getSouthWest().lat);
            document.getElementById("sw_longitude").value = Math.floor(bounds.getSouthWest().lng);
            document.getElementById("ne_latitude").value = Math.ceil(bounds.getNorthEast().lat);
            document.getElementById("ne_longitude").value = Math.ceil(bounds.getNorthEast().lng);
        });
        areaSelect.addTo(mymap);
    }

    function init_google_map() {
        map = new google.maps.Map(document.getElementById('map'), {
            center: {lat: 4.1, lng: -72.8},
            zoom: 5,
            mapTypeId: google.maps.MapTypeId.HYBRID,
        });

        var bounds = {
            north: 8.0,
            south: 4.0,
            east: -70.0,
            west: -75.7
        };

        rectangle = new google.maps.Rectangle({
            bounds: bounds,
            editable: true,
            draggable: true,
            strokeColor: '#FF0000',
            fillColor: '#FF0000',
        });

        rectangle.setMap(map);

        // Add an event listener on the rectangle.
        rectangle.addListener('bounds_changed', showNewRect);
        
        //Assign default values to the latitude and longitude inputs
        showNewRect(undefined);
    }

    /** @this {google.maps.Rectangle} */
    function showNewRect(event) {
        var ne = rectangle.getBounds().getNorthEast();
        var sw = rectangle.getBounds().getSouthWest();

        document.getElementById("sw_latitude").value = Math.floor(sw.lat());
        document.getElementById("sw_longitude").value = Math.floor(sw.lng());
        document.getElementById("ne_latitude").value = Math.ceil(ne.lat());
        document.getElementById("ne_longitude").value = Math.ceil(ne.lng());

    }
    
    function changeRectBounds(){
        var bounds = {
            north: Math.floor(document.getElementById("ne_latitude").value),
            south: Math.floor(document.getElementById("sw_latitude").value),
            east: Math.floor(document.getElementById("ne_longitude").value),
            west: Math.floor(document.getElementById("sw_longitude").value)
        };
        rectangle.setBounds(bounds);
    }
    
    
    // Getting the version id from the url and selecting it

    var pathArray = window.location.pathname.split('/');
    var versionIndex = pathArray.indexOf("version");
    var versionValue = null;
    if (versionIndex > 0) {
        versionValue = pathArray[versionIndex + 1];
        $('#id_version').val(versionValue);
    }

    // Reloading the web when the version changes

    $('#id_version').on('change', function () {
        var selectedIndex = this.selectedIndex;
        var algorithmIndex = pathArray.indexOf("new");
        if (selectedIndex > 0){
            var algorithmValue= pathArray[algorithmIndex + 1];
            var versionValue = this.options[this.selectedIndex].value;
            if(versionValue){
                var new_url = "/execution/new/"+algorithmValue+"/version/"+versionValue;
                window.location = new_url;
            }
            else{
                window.location = window.location + "version/" + this.options[this.selectedIndex].value;
            }
        }
    });

    $.ajax({
        url: "/execution/parameters/" + versionValue + "/",
        data: {
            format: 'json'
        },
        error: function () {
            console.log('Cant load the parameters.');
        },
        dataType: 'json',
        success: function (data) {
            console.log("Loading parameters for version " + versionValue + " of the algorithm.");
            console.log(data);
            createForm(data);
        },
        type: 'GET'
    });

    function getBands(storageUnitSelected, elementId){
        if (typeof(storageUnitSelected) !== 'number'){
            var element = this.id;
            storageUnitSelected = this.options[this.selectedIndex].value;
            elementId = element.split('_')[2];
        }
        $.post("/storage/json", {'storage_unit_id': storageUnitSelected}, function (data) {
            console.log('Getting the bands for the storage unit ' + storageUnitSelected + ' ... ');
            $('#bands_'+elementId).empty();
            var bands = data.metadata.measurements;
            var bands_select = document.getElementById("bands_"+elementId);
            var band_option = document.createElement("option");
            for (var i = 0 ; i < bands.length ; i++){
                band_option = document.createElement("option");
                band_option.value = bands[i].name;
                band_option.text = bands[i].name;
                bands_select.appendChild(band_option);
            }
        });
    }

    function createForm(json) {
        // obtaining the form
        var f = document.getElementById("mainForm");
        // iterating over the parameters
        jQuery.each(json, function (i, parameter) {
            var input_description = "";
            var parameter_type = parameter.fields.parameter_type;
            var pk = parameter.pk;
            var requiredText = (parameter.fields.required ? " <span class='text-danger small'> *</span>":"");
            if (parameter.fields.description !== ""){
                input_description = " <a class='help-hover hidden-xs hidden-sm hidden-md'><i class='glyphicon glyphicon-exclamation-sign' data-toggle='tooltip' data-placement='right' title='"+parameter.fields.description+"'></i></a>"
            }
            switch (parameter_type) {
                case "1":
                    console.log("Creating String field");
                    var string_input = document.createElement("input");
                    string_input.type = "text";
                    string_input.placeholder = parameter.fields.help_text;
                    string_input.id = "string_input_"+pk;
                    string_input.name = "string_input_"+pk;
                    string_input.className = "form-control";
                    string_input.required = parameter.fields.required;
                    string_input.value = parameter.fields.default_value;
                    // ===== LABELS =====
                    var label_string_title = document.createElement("label");
                    label_string_title.innerHTML = "<b>"+parameter.fields.name+requiredText+input_description+"</b>";
                    // ===== Paragraphs =====
                    var string_text = document.createElement("p");
                    string_text.innerHTML = parameter.fields.help_text;
                    string_text.className = "help-block";
                    // ===== DIVs =====
                    var param_div = document.createElement("div");
                    param_div.className = "form-group";
                    // appending everything
                    param_div.appendChild(label_string_title);
                    param_div.appendChild(string_input);
                    param_div.appendChild(string_text);
                    // appending to the form
                    f.appendChild(param_div);
                    break;
                case "2":
                    console.log("Creating IntegerType field");
                    var integer_input = document.createElement("input");
                    integer_input.type = "number";
                    integer_input.placeholder = parameter.fields.help_text;
                    integer_input.id = "integer_input_"+pk;
                    integer_input.name = "integer_input_"+pk;
                    integer_input.className = "form-control";
                    integer_input.required = parameter.fields.required;
                    integer_input.value = parameter.fields.default_value;
                    // ===== LABELS =====
                    var label_integer_title = document.createElement("label");
                    label_integer_title.innerHTML = "<b>"+parameter.fields.name+requiredText+input_description+"</b>";
                    // ===== Paragraphs =====
                    var integer_text = document.createElement("p");
                    integer_text.innerHTML = parameter.fields.help_text;
                    integer_text.className = "help-block";
                    // ===== DIVs =====
                    var param_div = document.createElement("div");
                    param_div.className = "form-group";
                    // appending everything
                    param_div.appendChild(label_integer_title);
                    param_div.appendChild(integer_input);
                    param_div.appendChild(integer_text);
                    // appending to the form
                    f.appendChild(param_div);
                    break;
                case "3":
                    console.log("Creating Double field");
                    var double_input = document.createElement("input");
                    double_input.type = "number";
                    double_input.step = "any";
                    double_input.placeholder = parameter.fields.help_text;
                    double_input.id = "double_input_"+pk;
                    double_input.name = "double_input_"+pk;
                    double_input.className = "form-control";
                    double_input.required = parameter.fields.required;
                    double_input.value = parameter.fields.default_value;
                    // ===== LABELS =====
                    var label_double_title = document.createElement("label");
                    label_double_title.innerHTML = "<b>"+parameter.fields.name+requiredText+input_description+"</b>";
                    // ===== Paragraphs =====
                    var double_text = document.createElement("p");
                    double_text.innerHTML = parameter.fields.help_text;
                    double_text.className = "help-block";
                    // ===== DIVs =====
                    var param_div = document.createElement("div");
                    param_div.className = "form-group";
                    // appending everything
                    param_div.appendChild(label_double_title);
                    param_div.appendChild(double_input);
                    param_div.appendChild(double_text);
                    // appending to the form
                    f.appendChild(param_div);
                    break;
                case "4":
                    console.log("Creating BooleanType field");
                    var boolean_input = document.createElement("input");
                    boolean_input.type = "checkbox";
                    boolean_input.placeholder = parameter.fields.help_text;
                    boolean_input.id = "boolean_input_"+pk;
                    boolean_input.name = "boolean_input_"+pk;
                    // ===== Bold =====
                    var boolean_name = document.createElement("B");
                    boolean_name.innerHTML = " <b>"+parameter.fields.name+requiredText+input_description+"</b>";
                    // ===== Paragraphs =====
                    var boolean_text = document.createElement("p");
                    boolean_text.innerHTML = parameter.fields.help_text;
                    boolean_text.className = "help-block";
                    // ===== DIVs =====
                    var param_div = document.createElement("div");
                    param_div.className = "form-group";
                    // appending everything
                    param_div.appendChild(boolean_input);
                    param_div.appendChild(boolean_name);
                    param_div.appendChild(boolean_text);
                    // appending to the form
                    f.appendChild(param_div);
                    break;
                case "7":
                    console.log("Creating AreaType field");
                    // ===== INPUTS =====
                    // sw latitude point
                    var sw_latitude_1 = document.createElement("input");
                    sw_latitude_1.type = "number";
                    sw_latitude_1.id = "sw_latitude";
                    sw_latitude_1.name = "sw_latitude";
                    sw_latitude_1.className = "form-control";
                    sw_latitude_1.required = parameter.fields.required;
                    sw_latitude_1.addEventListener("mouseup",function(){changeRectBounds()});
                    sw_latitude_1.addEventListener("keyup",function(){changeRectBounds()});	
                    // sw longitude point
                    var sw_longitude_1 = document.createElement("input");
                    sw_longitude_1.type = "number";
                    sw_longitude_1.id = "sw_longitude";
                    sw_longitude_1.name = "sw_longitude";
                    sw_longitude_1.className = "form-control";
                    sw_longitude_1.required = parameter.fields.required;
                    sw_longitude_1.addEventListener("mouseup",function(){changeRectBounds()});
                    sw_longitude_1.addEventListener("keyup", function(){changeRectBounds()});
                    // ne latitude point
                    var ne_latitude_2 = document.createElement("input");
                    ne_latitude_2.type = "number";
                    ne_latitude_2.id = "ne_latitude";
                    ne_latitude_2.name = "ne_latitude";
                    ne_latitude_2.className = "form-control";
                    ne_latitude_2.required = parameter.fields.required;
                    ne_latitude_2.addEventListener("mouseup",function(){changeRectBounds()});
                    ne_latitude_2.addEventListener("keyup", function(){changeRectBounds()});
                    // ne longitude point
                    var ne_longitude_2 = document.createElement("input");
                    ne_longitude_2.type = "number";
                    ne_longitude_2.id = "ne_longitude";
                    ne_longitude_2.name = "ne_longitude";
                    ne_longitude_2.className = "form-control";
                    ne_longitude_2.required = parameter.fields.required;
                    ne_longitude_2.addEventListener("mouseup",function(){changeRectBounds()});
                    ne_longitude_2.addEventListener("keyup", function(){changeRectBounds()});
                    // ===== LABELS =====
                    var label_sw_latitude_1 = document.createElement("label");
                    label_sw_latitude_1.innerHTML = "<b>Latitud mínima</b>";
                    var label_sw_longitude_1 = document.createElement("label");
                    label_sw_longitude_1.innerHTML = "<b>Longitud mínima</b>";
                    var label_ne_latitude_2 = document.createElement("label");
                    label_ne_latitude_2.innerHTML = "<b>Latitud máxima</b>";
                    var label_ne_longitude_2 = document.createElement("label");
                    label_ne_longitude_2.innerHTML = "<b>Longitud máxima</b>";
                    var area_title = document.createElement("label");
                    area_title.innerHTML = "<b>Mapa"+requiredText+input_description+"</b>";
                    // ===== Paragraphs =====
                    var area_text = document.createElement("p");
                    area_text.innerHTML = parameter.fields.help_text;
                    area_text.className = "help-block";
                    // ===== DIVs =====
                    var left_div = document.createElement("div");
                    left_div.className = "col-md-6 col-sm-6 col-xs-6";
                    var right_div = document.createElement("div");
                    right_div.className = "col-md-6 col-sm-6 col-xs-6";
                    var map_div = document.createElement("div");
                    map_div.className = "align-center";
                    map_div.id = "map";
                    map_div.style = "width: 550px; height: 400px;";
                    var param_div = document.createElement("div");
                    param_div.className = "form-group";
                    // appending everything
                    left_div.appendChild(label_sw_latitude_1);
                    left_div.appendChild(sw_latitude_1);
                    left_div.appendChild(label_sw_longitude_1);
                    left_div.appendChild(sw_longitude_1);
                    right_div.appendChild(label_ne_latitude_2);
                    right_div.appendChild(ne_latitude_2);
                    right_div.appendChild(label_ne_longitude_2);
                    right_div.appendChild(ne_longitude_2);
                    param_div.appendChild(area_title);
                    param_div.appendChild(map_div);
                    param_div.appendChild(area_text);
                    param_div.appendChild(left_div);
                    param_div.appendChild(right_div);
                    // appending to the form
                    f.appendChild(param_div);
                    init_google_map();
                    break;
                case "8":
                    console.log("Creating StorageUnitType field");
                    // creating initial divs
                    var tmp_storage = document.createElement("div");
                    var tmp_bands = document.createElement("div");
                    tmp_storage.id = "storage_band_div";
                    tmp_bands.id = "band_div";
                    f.appendChild(tmp_storage);
                    f.appendChild(tmp_bands);
                    //getting the json
                    $.getJSON( "/storage/storage_units", function( su_data ) {
                        // storage_unit_select
                        var storage_unit_select = document.createElement("select");
                        storage_unit_select.id = "storage_unit_"+pk;
                        storage_unit_select.name = "storage_unit_"+pk;
                        storage_unit_select.className = "form-control";
                        storage_unit_select.onchange = getBands;
                        // storage_unit_options
                        var storage_unit_option = document.createElement("option");
                        jQuery.each(su_data, function (i, storage_unit_value) {
                            var storage_pk = storage_unit_value.pk;
                            var storage_name = storage_unit_value.fields.name;
                            storage_unit_option = document.createElement("option");
                            storage_unit_option.value = storage_pk;
                            storage_unit_option.text = storage_name;
                            storage_unit_select.appendChild(storage_unit_option);
                        });
                        // bands_select
                        var bands_select = document.createElement("select");
                        bands_select.id = "bands_"+pk;
                        bands_select.name = "bands_"+pk;
                        bands_select.className = "form-control";
                        bands_select.multiple = true;
                        bands_select.required = parameter.fields.required;
                        bands_select.size = 8;
                        // ===== LABELS =====
                        var storage_unit_label = document.createElement("label");
                        storage_unit_label.innerHTML = "<b>Posibles unidades de almacenamiento origen"+requiredText+input_description+"</b>";
                        var band_label = document.createElement("label");
                        band_label.innerHTML = "<b>Bandas de compuesto</b>";
                        // ===== Paragraphs =====
                        var storage_bands_text = document.createElement("p");
                        storage_bands_text.innerHTML = parameter.fields.help_text;
                        storage_bands_text.className = "help-block";
                        // ===== DIVs =====
                        var storage_unit_param_div = document.getElementById("storage_band_div");
                        storage_unit_param_div.className = "form-group";
                        var band_param_div = document.getElementById("band_div");
                        band_param_div.className = "form-group";
                        // appending everything
                        storage_unit_param_div.appendChild(storage_unit_label);
                        storage_unit_param_div.appendChild(storage_unit_select);
                        band_param_div.appendChild(band_label);
                        band_param_div.appendChild(bands_select);
                        band_param_div.appendChild(storage_bands_text);
                        // getting the bands for the storage unit;
                        getBands(su_data[0].pk, pk);
                    });
                    break;
                case "9":
                    console.log("Creating TimePeriod field");
                    // start date
                    var start_date_input = document.createElement("input");
                    start_date_input.id = "start_date_"+pk;
                    start_date_input.name = "start_date_"+pk;
                    start_date_input.className = "form-control datepicker";
                    start_date_input.required = parameter.fields.required;
                    // end date
                    var end_date_input = document.createElement("input");
                    end_date_input.id = "end_date_"+pk;
                    end_date_input.name = "end_date_"+pk;
                    end_date_input.className = "form-control datepicker";
                    end_date_input.required = parameter.fields.required;
                    // ===== LABELS =====
                    var start_date_label = document.createElement("label");
                    start_date_label.innerHTML = "<b>Desde</b>";
                    var end_date_label = document.createElement("label");
                    end_date_label.innerHTML = "<b>Hasta</b>";
                    // ===== Paragraphs =====
                    var paragraph_title = document.createElement("p");
                    paragraph_title.innerHTML = "<b>Periodo de consulta"+requiredText+input_description+"</b>";
                    var paragraph_text = document.createElement("p");
                    paragraph_text.innerHTML = parameter.fields.help_text;
                    paragraph_text.className = "help-block";
                    // ===== DIVs =====
                    var left_div = document.createElement("div");
                    left_div.className = "col-md-6";
                    var right_div = document.createElement("div");
                    right_div.className = "col-md-6";
                    var param_div = document.createElement("div");
                    param_div.className = "form-group";
                    // appending everything
                    left_div.appendChild(start_date_label);
                    left_div.appendChild(start_date_input);
                    right_div.appendChild(end_date_label);
                    right_div.appendChild(end_date_input);
                    param_div.appendChild(paragraph_title);
                    param_div.appendChild(left_div);
                    param_div.appendChild(right_div);
                    param_div.appendChild(paragraph_text);
                    // appending to the form
                    f.appendChild(param_div);
                    break;
                case "12":
                    console.log("Creating File field");
                    var file_input = document.createElement("input");
                    file_input.type = "file";
                    file_input.id = "file_input_"+pk;
                    file_input.name = "file_input_"+pk;
                    file_input.className = "form-control";
                    file_input.required = parameter.fields.required;
                    file_input.accept = ".zip";
                    // ===== LABELS =====
                    var label_file_title = document.createElement("label");
                    label_file_title.innerHTML = "<b>"+parameter.fields.name+requiredText+input_description+"</b>";
                    // ===== Paragraphs =====
                    var file_text = document.createElement("p");
                    file_text.innerHTML = parameter.fields.help_text;
                    file_text.className = "help-block";
                    // ===== DIVs =====
                    var param_div = document.createElement("div");
                    param_div.className = "form-group";
                    // appending everything
                    param_div.appendChild(label_file_title);
                    param_div.appendChild(file_input);
                    param_div.appendChild(file_text);
                    // appending to the form
                    f.appendChild(param_div);
                    break;
                case "13":
                    console.log("Creating StorageUnitType (no bands) field");
                    // creating initial divs
                    var tmp_storage = document.createElement("div");
                    tmp_storage.id = "storage_nb_div";
                    f.appendChild(tmp_storage);
                    //getting the json
                    $.getJSON( "/storage/storage_units", function( su_data ) {
                        // storage_unit_select
                        var storage_unit_select = document.createElement("select");
                        storage_unit_select.id = "storage_unit_"+pk;
                        storage_unit_select.name = "storage_unit_"+pk;
                        storage_unit_select.className = "form-control";
                        // storage_unit_options
                        var storage_unit_option = document.createElement("option");
                        jQuery.each(su_data, function (i, storage_unit_value) {
                            var storage_pk = storage_unit_value.pk;
                            var storage_name = storage_unit_value.fields.name;
                            storage_unit_option = document.createElement("option");
                            storage_unit_option.value = storage_pk;
                            storage_unit_option.text = storage_name;
                            storage_unit_select.appendChild(storage_unit_option);
                        });
                        // ===== LABELS =====
                        var storage_unit_label = document.createElement("label");
                        storage_unit_label.innerHTML = "<b>Posibles unidades de almacenamiento origen"+requiredText+input_description+"</b>";
                        // ===== Paragraphs =====
                        var storage_no_band_text = document.createElement("p");
                        storage_no_band_text.innerHTML = parameter.fields.help_text;
                        storage_no_band_text.className = "help-block";
                        // ===== DIVs =====
                        var storage_unit_param_div = document.getElementById("storage_nb_div");
                        storage_unit_param_div.className = "form-group";
                        // appending everything
                        storage_unit_param_div.appendChild(storage_unit_label);
                        storage_unit_param_div.appendChild(storage_unit_select);
                        storage_unit_param_div.appendChild(storage_no_band_text);
                    });
                    break;
                default:
                    console.log("Object not supported, " + parameter_type);
            }
        });
        console.log("Configuring datepicker");
        $('.datepicker').datepicker({
            format: "dd/mm/yyyy",
            language: "es",
            autoclose: true,
            todayHighlight: true
        });
        executed_params = JSON.parse(executed_params);
        console.log(executed_params);
        for(var i = 0, length = executed_params.length; i< length; i++)
        {
            var param = executed_params[i];
            console.log("parametro: ");
            console.log(param);
            switch(param.parameter_type)
            {
                case "1":
                    document.getElementById("string_input_"+param.parameter_pk).value = param.value;
                    break;
                case "2":
                    document.getElementById("integer_input_"+param.parameter_pk).value = param.value;
                    break;
                case "3":
                    document.getElementById("double_input_"+param.parameter_pk).value = param.value;
                    break;
                case "4":
                    document.getElementById("boolean_input_"+param.parameter_pk).checked = param.value == "True";
                    break;
                case "7":
                    document.getElementById("sw_latitude").value = param.latitude_start;
                    document.getElementById("sw_longitude").value = param.longitude_start;
                    document.getElementById("ne_latitude").value = param.latitude_end;
                    document.getElementById("ne_longitude").value = param.longitude_end;
                    changeRectBounds();
                    break;
                case "8":
                    var intervalId = setInterval(function(){
                        var storage_unit_selector = document.getElementById("storage_unit_"+param.parameter_pk);
                        if(storage_unit_selector)
                        {
                            for(var i = 0,
                                length = storage_unit_selector.length,
                                notFinished = true,
                                options = storage_unit_selector.options; i < length && notFinished; i++)
                            {
                                if(options[i].text === "LS7_ETM_LEDAPS")//param.storage_unit_name)
                                {
                                    storage_unit_selector.selectedIndex = i;
                                    notFinished = false;
                                }
                            }
                            clearInterval(intervalId);
                        }
                    }, 100);
                    break;
                case "9":
                    break;
                case "12":
                    break;
                case "13":
                    break;
                default:
                    break;
            }
        }

        console.log("Creating Send Button");
        var send_button = document.createElement("button");
        send_button.type = "submit";
        send_button.className = "btn btn-default";
        send_button.innerHTML = "Ejecutar Algoritmo";
        var param_div = document.createElement("div");
        param_div.className = "text-center";
        // appending the button
        param_div.appendChild(send_button);
        f.appendChild(param_div);
        // appending the custom form
        $("mainForm").append(f);
    };
});
