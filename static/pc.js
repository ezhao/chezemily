function submitAnswer(question, answer) {
    $.ajax({
        type: "POST",
        url: "/pc/answer",
        data: { question: question, answer: answer }
    });
}

function submitAnswerNext(question, answer, nextPage) {
    $.ajax({
        type: "POST",
        url: "/pc/answer",
        data: { question: question, answer: answer },
        success: function(result) {
            window.location.href = result;
        }
    });
}

$(function() {
    $(".div-avatar").click(function() {
        var avatars = $(".div-avatar");
        for (i=0; i < avatars.length; i++) {
            if (avatars[i] == this) {
                this.classList.add("div-avatar-selected");
            } else {
                avatars[i].classList.remove("div-avatar-selected");
            }
        }
        var pcQuestion = "Avatar";
        var pcAnswer = this.getAttribute("pc-answer");
        submitAnswer(pcQuestion, pcAnswer);
        $(".pc-blue-button").show();
    });

    $(".img-activity").click(function() {
        var pcQuestion = "Activities";
        var pcAnswer = [];
        window.A = this;
        if (this.classList.contains("img-activity-selected")) {
            this.classList.remove("img-activity-selected");
        } else {
            this.classList.add("img-activity-selected");
        }
        $.each($(".img-activity-selected"), function(){
             pcAnswer.push(this.getAttribute('pc-answer'));
        });
        submitAnswer(pcQuestion, pcAnswer.join(', '));
    });

    $(".div-day").click(function() {
        var days = $(".div-day");
        for (i=0; i < days.length; i++) {
            if (days[i] == this) {
                this.classList.add("div-day-selected");
            } else {
                days[i].classList.remove("div-day-selected");
            }
        }
        var pcQuestion = "Day";
        var pcAnswer = this.getAttribute("pc-answer");
        submitAnswer(pcQuestion, pcAnswer);
        $(".pc-blue-button").show();
    });

    $(".li-train").hover(function() {
        this.classList.add('li-train-selected');
        $(this).children(".div-train-top").children("span").show();
    }, function() {
        this.classList.remove('li-train-selected');
        $(this).children(".div-train-top").children("span").hide();
    });

    $(".li-train").click(function() {
        var things = $(".li-train");
        for (i=0; i < things.length; i++) {
            if (things[i] == this) {
                this.classList.add("li-train-selected");
            } else {
                things[i].classList.remove("li-train-selected");
            }
        }
        var pcQuestion = "Train";
        var pcAnswer = this.getAttribute("pc-answer");
        submitAnswer(pcQuestion, pcAnswer);
        $.each($(".li-train-really-selected"), function(){
             this.classList.remove('li-train-really-selected');
        });
        this.classList.add("li-train-really-selected");
        $(".pc-blue-button").show();
    });

    $("#quiz-foodlike").on('change keyup paste', function(e) {
        var pcQuestion = "Foods liked";
        var pcAnswer = e.target.value;
        submitAnswer(pcQuestion, pcAnswer);
    });

    $("#quiz-fooddislike").on('change keyup paste', function(e) {
        var pcQuestion = "Foods disliked";
        var pcAnswer = e.target.value;
        submitAnswer(pcQuestion, pcAnswer);
    });
    
    $(".checkbox").click(function() {
        var pcQuestion = "Drinks";
        var pcAnswer = []
        $.each($("input:checked"), function(){            
             pcAnswer.push($(this.parentElement).text());
        });
        submitAnswer(pcQuestion, pcAnswer.join(', '));
    })
});
