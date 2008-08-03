emlprime = typeof emlprime == 'undefined' ? {} : emlprime;
emlprime.play = function () {
    var self = {
        key_sequence: [],
        clicked_sequence: [],
	playback_position: 0,
        click_delay_limit: 5000,  // 5 second pause between clicks
        playback_delay: 1000,     // 1 second pause between lighting up on playback
        set_on: function(color) {
            // light up a light of the appropriate color
	    var button = $("#game #" + color + " img"),
	        tokens = button.attr("src").split("."),
	        src = tokens[0],
	        suffix = tokens[1],
	        src_on = src+"_light."+suffix;
    
	    button.attr("src", src_on);
	    var t = setTimeout(function () { self.set_off(color); }, self.playback_delay);
        },
	set_off: function(color) {
	    // turn of the light
	    var button = $("#game #" + color + " img"),
	    src_off = button.attr("src").replace("_light","");
	    button.attr("src", src_off);
	},
	click_handler: function (event) {
	    self.clicked_sequence.push($(event.target).attr('alt'));
	    console.log(self.clicked_sequence);
	},
	load_answer_key: function(data) {
	    console.log(data);
	    self.key_sequence = data;
	}
    }
    return self;
}();


function assign_behaviors() {
    $('#game img').unbind("click").bind("click", emlprime.play.click_handler);
    $.getJSON("/play/get_answer_key/", emlprime.play.load_answer_key);
}
    
$(document).ready(assign_behaviors);
