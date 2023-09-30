$(document).ready(
    function () {
        $("#posts_list").click(function () {
            $.ajax({
                url: '/my-endpoint?mode=2',
                type: 'get',
                success: function (response) {
                    $("#myDiv").addClass(response);
                }
            });
        });
    },
);