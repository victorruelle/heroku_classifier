// One-piece loader
// Host website : https://read-onepiece.com/

// $(document).ready(function () {
//     $("#LastOnePieceChapter").text("208")
// });

const url = "https://1.bp.blogspot.com/-5llV_yu1aT4/XqNgCvvPImI/AAAAAAAAj94/WXMDgg3STaUAKiXQppgM_yvTwxkcSYf5ACLcBGAsYHQ/s1600/one_piece_978_1.jpg";

$(document).ready(function () {
    $("#loadNext").click(function (e) {
        $("#currentImage").attr("src",url)
    });
});