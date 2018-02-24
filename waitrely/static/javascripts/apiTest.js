// jQuery.noConflict();

var $ = jQuery;


$(document).ready(function () {

    function removeOldElement(parentID, childID) {

        var parent = document.getElementById(parentID);
        var child = document.getElementById(childID);

        if (child !== null) {
            parent.removeChild(child);
        }
    }

    function displayJson(obj, resultID) {

        var resultTable = resultID + "-table";

        removeOldElement(resultID, resultTable);

        var tableContainer = $("#" + resultID);

        var tbl = $("<table id='" + resultTable + "'" + "></table>");

        tbl.append("<tbody>");

        var tr = "<tr>";

        var titleAurn = "<td class='head-table'>Udprn</td>";
        var titleAddressFull = "<td class='head-table'>Full address</td>";
        var titlePostcode = "<td class='head-table'>Postcode</td>";
        var tre = "<tr>";

        tbl.append(tr + titleAurn + titleAddressFull + titlePostcode + tre);

        var addressIndex = 0;

        var addresses = "address" + addressIndex;

        while (obj[addresses] !== undefined) {

            var td1 = "<td class='aurn-field'>" + "<span class='aurn-field-span' value='" + obj[addresses]["udprn"] + "'>" + obj[addresses]["udprn"] + "</span></td>";
            var td2 = "<td class='address-field'>" + obj[addresses]["l0_full_address"] + "</td>";
            var td3 = "<td class='postcode-field'>" + obj[addresses]["l0_postcode"] + "</td></tr>";
            tbl.append(tr + td1 + td2 + td3);

            addressIndex = addressIndex + 1;
            addresses = "address" + addressIndex;

        }

        tbl.append("</tbody>");

        $("#" + resultID).append(tbl);
    }

    /**
     * @return {boolean}
     */
    function IsJsonString(str) {
        try {
            JSON.parse(str);
        } catch (e) {
            return false;
        }
        return true;
    }

    var apiKeyPass = "";

    function displayApiInfo(data) {
        if (data !== null) {

            var apiInfo = $('#apiInfo');

            if (apiInfo.text() !== "") {
                apiInfo.text("");
            }

            // apiInfo.append("<hr class='style-two'>");

            apiInfo.append('<span>' + "Limit per month: " + data["limit-month"] + " | " + '</span>');
            apiInfo.append('<span>' + "Remaining for this month: " + data["remaining-month"] + '</span>');
            apiInfo.append('<br>');
            apiInfo.append('<span>' + "Limit per minute: " + data["limit-minute"] + " | " + '</span>');
            apiInfo.append('<span>' + "Remaining for this minute: " + data["remaining-minute"] + '</span>');

            // apiInfo.append("<hr class='style-two'>");

        }
    }

    function callAPI(buttonID, formID, resultID, table) {

        var sendApi = $('a#' + buttonID);

        var sendApiForm = $(formID);

        var apiKey = sendApi.bind('click', function () {

            var url = $('#' + formID + ' p.display-url').text();

            apiKeyPass = $('#' + formID + ' input[name="apikey-in"]').val();

            $.getJSON($SCRIPT_ROOT + '/_apiQuery', {
                apiQ0: url,
                apiQ1: apiKeyPass,
                apiQ2: $('#' + formID + ' input[name="string-in"]').val(),
                apiQ3: $('#' + formID + ' input[name="page-in"]').val()

            }, function (data) {

                    displayApiInfo(data[1]);

                if (table) {

                    displayJson(data[0], resultID);

                } else {
                    // document.getElementById(resultID).innerHTML = JSON.stringify(data, undefined, 2);

                    removeOldElement(resultID, "udprn-json");

                    document.getElementById(resultID).appendChild(
                        renderjson(data[0]));

                    var openFirstLine = document.getElementsByClassName("disclosure");

                    openFirstLine[0].click();

                }

            });

            return false;

        });
    }

    function callSecondAPI(ver, formID) {

        $(document).on('click', ver, function () {

            var postcode = $(this).attr('value');

            $('#' + formID + ' input[name="apikey-in"]').val(apiKeyPass);
            $('#' + formID + ' input[name="string-in"]').val(postcode);

            $('html, body').animate({
                scrollTop: $("#find-address-by-udprn").offset().top
            }, 2000);

        });
    }

    callAPI("sendApi", "sendApi-form", "result", true);

    callSecondAPI('.aurn-field-span', "sendApi1-form");

    callAPI("sendApi1", "sendApi1-form", "jsonResultUDPRN", false);


    $('#page-in, #string-in').keydown(function (event) {
        // enter has keyCode = 13, change it if you want to use another button
        if (event.keyCode === 13) {

            $("a#sendApi").click();
            // $("a#sendApi1").click();
        }
    });


//    end of the script


});

