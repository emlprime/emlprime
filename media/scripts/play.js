emlprime = typeof emlprime == 'undefined' ? {} : emlprime;
emlprime.play = function () {
    var self = {
        key_sequence: [],
        clicked_sequence: [],
	game_over: false,
	playback_position: 0,
	playback_limit: 1,
        click_delay_limit: 3000,  // 3 second pause between clicks
	click_delay_id: undefined, //sets the timer id for the click delay to undefined
	playback_delay_id: undefined, //sets the timer id for the playback delay to undefined
        playback_delay: 300,     // brief pause between lighting up on playback
	switch_playback_mode_delay: 1500, // short pause between the last click and playing back the next set
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
	    if (typeof callback != 'undefined') {
		self.playback_delay_id = setTimeout(function () { callback(); }, self.playback_delay);
	    }
	},
	click_handler: function (event) {
	    var color = $(event.target).attr('alt');
	    self.clicked_sequence.push(color);
	    var result = self.evaluate_click();
	    if (result == false){
		self.end_game();
		return;
	    }
	    var playback_length = (self.playback_limit - 1), // We've already incremented playback limit
	        clicked_sequence_length = self.clicked_sequence.length;
	    
	    //console.log("clicked sequence length:" + clicked_sequence_length);
	    //console.log("playback length:" + playback_length);
	    //console.log(clicked_sequence_length >= playback_length);

	    if (clicked_sequence_length >= playback_length) {
		$('#game img').unbind("click");
		callback = self.playback;
		self.clicked_sequence = [];
	    } else {
		//console.log("unbind");
		callback = undefined;
	    }
	    //console.log(callback);
	    self.set_on(color, callback);

	    //console.log(self.clicked_sequence);
	},
	evaluate_click: function() {
	    for (var i = 0; i < self.clicked_sequence.length; i++) {
		if (self.key_sequence[i] != self.clicked_sequence[i]) {
		    return false;
		    }
		}
	    clearTimeout(self.click_delay_id);
	    self.click_delay_id = setTimeout(function () {self.end_game();}, self.click_delay_limit)
	    return true;
	},
	end_game: function() {
	    clearTimeout(self.playback_delay_id);
	    clearTimeout(self.click_delay_id);
	    alert("Game Over!");
	    self.game_over = true;
	},
	load_answer_key: function(data) {
	    //console.info("got data from server");
	    console.log(data);
	    self.key_sequence = data;
	    self.playback();
	},
	playback: function() {
	    if (self.game_over == true) {
		return;
	    }
	    //console.info("playback");
	    //console.log("position:"+self.playback_position);
	    //console.log("limit:"+self.playback_limit);
	    if (self.playback_limit > self.key_sequence.length) {
		alert("You win!");
		clearTimeout(self.playback_delay_id);
		clearTimeout(self.click_delay_id);
		return;
	    }
	    var delay = (self.playback_position == 0) ? self.switch_playback_mode_delay : 0;
	    if (self.playback_position < self.playback_limit) {
		clearTimeout(self.click_delay_id);
		self.playback_delay_id = setTimeout(function () {
			self.set_on(self.key_sequence[self.playback_position], self.playback);
			self.playback_position += 1;
		    },
		    delay
		    );
	    } else {
		self.playback_position = 0;
		self.playback_limit += 1;
		$('#game img').unbind("click").bind("click", self.click_handler);
		clearTimeout(self.click_delay_id);
		self.click_delay_id = setTimeout(function () {self.end_game();}, self.click_delay_limit)
	    }
	},
	start_game: function() {
	    self.clicked_sequence = [];
	    self.playback_limit = 1;
	    self.playback_position = 0;
	    self.game_over = false;
	    $.getJSON("/play/get_answer_key/", self.load_answer_key);	
	}
    }
    return self;
}();

function assign_behaviors() {
    //console.log("starting");
    $('#start_game').unbind('click').bind('click', emlprime.play.start_game);
}
    
$(document).ready(assign_behaviors);
