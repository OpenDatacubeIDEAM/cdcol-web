/* Custom Form Builder
 * Author:Manre
 * Author e-mail:nobmann88@gmail.com
 * Version:0.1
 * Created:October 2016
 * File Description: This class will modify the page to create a custom form
 */

$(document).ready(function () {

    $.ajax({
        url: 'http://localhost:8000/execution/parameters/12/',
        data: {
            format: 'json'
        },
        error: function () {
            console.log('Cant load the parameters.');
        },
        dataType: 'json',
        success: function (data) {
            createForm(data);
        },
        type: 'GET'
    });

    function createForm(json) {
        console.log(json);
        // obtaining the form
        var f = document.getElementById("mainForm");
        // iterating over the parameters
        jQuery.each(json, function (i, parameter) {
            var parameter_type = parameter.fields.parameter_type;
            var pk = parameter.pk;
            switch (parameter_type) {
                case "7":
                    console.log("Creating AreaType field");
                    // ===== INPUTS =====
                    // sw latitude point
                    var sw_latitude_1 = document.createElement("input");
                    sw_latitude_1.type = "text";
                    sw_latitude_1.id = "sw_latitude_"+pk;
                    sw_latitude_1.name = "sw_latitude_"+pk;
                    sw_latitude_1.className = "form-control";
                    // sw longitude point
                    var sw_longitude_1 = document.createElement("input");
                    sw_longitude_1.type = "text";
                    sw_longitude_1.id = "sw_longitude_"+pk;
                    sw_longitude_1.name = "sw_longitude_"+pk;
                    sw_longitude_1.className = "form-control";
                    // ne latitude point
                    var ne_latitude_2 = document.createElement("input");
                    ne_latitude_2.type = "text";
                    ne_latitude_2.id = "ne_latitude_"+pk;
                    ne_latitude_2.name = "ne_latitude_"+pk;
                    ne_latitude_2.className = "form-control";
                    // ne longitude point
                    var ne_longitude_2 = document.createElement("input");
                    ne_longitude_2.type = "text";
                    ne_longitude_2.id = "ne_longitude_"+pk;
                    ne_longitude_2.name = "ne_longitude_"+pk;
                    ne_longitude_2.className = "form-control";
                    // ===== LABELS =====
                    var label_sw_latitude_1 = document.createElement("label");
                    label_sw_latitude_1.innerHTML = "<b>Latitud SW</b>";
                    var label_sw_longitude_1 = document.createElement("label");
                    label_sw_longitude_1.innerHTML = "<b>Longitud SW</b>";
                    var label_ne_latitude_2 = document.createElement("label");
                    label_ne_latitude_2.innerHTML = "<b>Latitud NE</b>";
                    var label_ne_longitude_2 = document.createElement("label");
                    label_ne_longitude_2.innerHTML = "<b>Longitud NE</b>";
                    var area_title = document.createElement("label");
                    area_title.innerHTML = "<b>Mapa</b>";
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
                    param_div.appendChild(left_div);
                    param_div.appendChild(right_div);
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
                    // ===== LABELS =====
                    var label_integer_title = document.createElement("label");
                    label_integer_title.innerHTML = "<b>"+parameter.fields.name+"</b>";
                    // ===== DIVs =====
                    var param_div = document.createElement("div");
                    param_div.className = "form-group";
                    // appending everything
                    param_div.appendChild(label_integer_title);
                    param_div.appendChild(integer_input);
                    // appending to the form
                    f.appendChild(param_div);
                    break;
                case "9":
                    console.log("Creating TimePeriod field");
                    // start date
                    var start_date_input = document.createElement("input");
                    start_date_input.type = "date";
                    start_date_input.id = "start_date_"+pk;
                    start_date_input.name = "start_date_"+pk;
                    start_date_input.className = "form-control";
                    // end date
                    var end_date_input = document.createElement("input");
                    end_date_input.type = "date";
                    end_date_input.id = "end_date_"+pk;
                    end_date_input.name = "end_date_"+pk;
                    end_date_input.className = "form-control";
                    // ===== LABELS =====
                    var start_date_label = document.createElement("label");
                    start_date_label.innerHTML = "<b>Desde</b>";
                    var end_date_label = document.createElement("label");
                    end_date_label.innerHTML = "<b>Hasta</b>";
                    // ===== Paragraphs =====
                    var paragraph_title = document.createElement("p");
                    paragraph_title.innerHTML = "<b>Periodo de consulta</b>";
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
                case "8":
                    console.log("Creating StorageUnitType field");
                    // creating initial divs
                    var tmp_storage = document.createElement("div");
                    var tmp_bands = document.createElement("div");
                    tmp_storage.id = "storage_div";
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
                        // band_options
                        var band_option = document.createElement("option");
                        for (i = 0; i < 3; i++) {
                            band_option = document.createElement("option");
                            band_option.value = i;
                            band_option.text = "Banda " + i;
                            bands_select.appendChild(band_option);
                        }
                        // ===== LABELS =====
                        var storage_unit_label = document.createElement("label");
                        storage_unit_label.innerHTML = "<b>Posibles unidades de almacenamiento origen *</b>";
                        var band_label = document.createElement("label");
                        band_label.innerHTML = "<b>Bandas de compuesto</b>";
                        // ===== DIVs =====
                        var storage_unit_param_div = document.getElementById("storage_div");
                        storage_unit_param_div.className = "form-group";
                        var band_param_div = document.getElementById("band_div");
                        band_param_div.className = "form-group";
                        // appending everything
                        storage_unit_param_div.appendChild(storage_unit_label);
                        storage_unit_param_div.appendChild(storage_unit_select);
                        band_param_div.appendChild(band_label);
                        band_param_div.appendChild(bands_select);
                    });
                    break;
                case "4":
                    console.log("Creating BooleanType field");
                    var boolean_input = document.createElement("input");
                    boolean_input.type = "checkbox";
                    boolean_input.placeholder = parameter.fields.help_text;
                    boolean_input.id = "boolean_input_"+pk;
                    boolean_input.name = "boolean_input_"+pk;
                    //boolean_input.text = "<b>"+parameter.fields.name+"</b>";
                    // ===== Bold =====
                    var boolean_name = document.createElement("B");
                    boolean_name.innerHTML = " <b>"+parameter.fields.name+"</b>";
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
                default:
                    console.log("Object not supported");
            }
        });
        $("mainForm").append(f);
    };
});