emlprime = typeof emlprime == 'undefined' ? {} : emlprime;
emlprime.play = function () {
    var self = {
        key_sequence: [],
        clicked_sequence: [],
	playback_position: 0,
	playback_limit: 1,
        click_delay_limit: 5000,  // 5 second pause between clicks
        playback_delay: 500,     // 1 second pause between lighting up on playback
        set_on: function(color, callback) {
            // light up a light of the appropriate color
	    var button = $("#game #" + color + " img"),
	        tokens = button.attr("src").split("."),
	        src = tokens[0],
	        suffix = tokens[1],
	        src_on = src+"_light."+suffix;
    
	    button.attr("src", src_on);
	    // turn the light off after playback delay
	    var t = setTimeout(function () { self.set_off(color, callback); }, self.playback_delay);
        },
	set_off: function(color, callback) {
	    // turn of the light
	    var button = $("#game #" + color + " img"),
	    src_off = button.attr("src").replace("_light","");
	    button.attr("src", src_off);
	    if (self.playback_position < self.playback_limit) {
		self.playback_position += 1;
		}
	    if (typeof callback != 'undefined') {
		setTimeout(function () { callback(); }, self.playback_delay);
	    }
	},
	click_handler: function (event) {
	    var color = $(event.target).attr('alt');
	    console.log(self.clicked_sequence.length >= self.playback_limit);
	    if (self.clicked_sequence.length >= self.playback_limit) {
		callback = self.playback;
		self.playback_limit += 1;
		self.playback_position = 0;
	    } else {
		callback = undefined;
	    }
	    self.clicked_sequence.push(color);
	    
	    self.set_on(color, callback);
	    $('#game img').unbind("click");
	    self.playback_limit += 1;
	    console.log(self.clicked_sequence);
	},
	load_answer_key: function(data) {
	    console.info("got data from server");
	    console.log(data);
	    self.key_sequence = data;
	    self.playback();
	},
	playback: function() {
	    console.log("position:"+self.playback_position);
	    console.log("limit:"+self.playback_limit);
	    if (self.playback_position < self.playback_limit) {
		self.set_on(self.key_sequence[self.playback_position], self.playback);
	    } else {
		self.playback_position = 0;
		self.playback_limit += 1;
		$('#game img').unbind("click").bind("click", self.click_handler);
	    }
	}
    }
    return self;
}();

function assign_behaviors() {
    console.log("starting");
    $.getJSON("/play/get_answer_key/", emlprime.play.load_answer_key);
}
    
$(document).ready(assign_behaviors);
