WaitForSomeEventsCallback = function(eventCount, Callback)
{
	this.eventCount = eventCount;
	this.Callback = Callback;
	this.firedEvents = 0;
	this.trigger = function()
	{
		this.firedEvents += 1;
		if(this.firedEvents == this.eventCount)
			Callback();
	};
};