$(document).ready(function(){
    //Calling GET /e-link/templates does not return templates ordered by templateID. This function returns the right index for the .after() function below
    var insort =function (id) {
        for (var i=id-1;i>=0;i--) {
            if ($("#templateh"+i).length) {
                return i;
            }
        }
        return 0;
    };
    $.ajax({
        url: fremeApiUrl+"/e-link/templates",
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        method: 'GET',
        success: function (data) {
            $(data).each(
                function (i, template) {
                    //Ternary operator to add any Description to Templates without description in the database
                    (template.description == "") ? description = "This is template number " + template.templateId + " and it has no description in the database" : description = template.description;
                    var index = insort(template.templateId);
                    //Adds a templateOuter div containing a templateInner div for each template with all available information
                    $('#templatediv' + index).after(
                        "<h3  id=\"templateh" + template.templateId + "\">" + template.templateId + " - " + template.label +
                        "</h3>" +
                        "<div id=\"templatediv"+template.templateId+"\">"+
                            "<h4> Description: </h4>" +
                            "<div>" + description + "</div>" +
                            "<h4> SPARQL Endpoint: </h4>"+
                            "<div><code><a href=\""+template.endpoint+"\">" +template.endpoint+"</a></code></div>" +
                            "<h4> SPARQL Query: </h4>"+
                            "<div><pre><code>"+template.query+"</code></pre></div>" +
                        "</div>")


                });
            $(".ui-accordion-content").css(color="green");
            $("#templateh0 ").remove();
            $("#templatediv0").remove();
            $("#templates").accordion();
        }
    });
});
