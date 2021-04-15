# Required Features
- [x] Player aliasing. This will allow players to use alts, and rename their mains while maintaining constant stats
  - Issues exist with players aliasing accounts not their own. Solution: Players can only alias players they (or their guild) have permissions to query. Dealising is possible. Inter-team trolling isn't my problem.
  - An alias is simply a forwarding of player_ids. If a player has 2 account, or they change their name, an alias will allow querying of data for player_ids where player_id is the one they queries, or where a player_id matches an alias.

# Short-Term Planned Features

- [ ] Custom tagging for match (and therefore statistic) data. This will expand on the current hard-coded scrim, qual, and league tags.
  - Data can be broken down by tag, similar to now
  - Data is tagged when uploaded. If no tag is provided, then this data will only be seen in aggregates.
  - Allows teams to view their data for specific leagues, against specific teams, etc.
  - Data can be viewed on *multiple* tags. Ie, `=playerstats` will be allowed to be provided a list of tags and it will aggregate all data over these tags. If no tags are provided then it aggregates all data.
- [ ] The ability to only grab data for *n* most recent, or a range of *n* ago to *m* ago games. Specifically, range *n* to 0 is equivalent to *n* most recent.
  - This will allow teams to compare recent and old data.
  - This will allow teams to optionally view new data while preserving the old data.
- [ ] The ability to view statistics on matches that were played:
  - Map W/L.
  - Site W/L.
  - Map W/L when starting on attack.
  - Map avg rounds at half when starting on attack.
  - Map avg rounds at half when starting on defense.
- [ ] The ability to remove matches from *n* games ago and earlier (or a range of games from *n* ago to *m* ago.)

# Long-term Planned Features
- [ ] Custom website which will allow total skirting of the DiscordBot. This is for V1.0.0 [release] which will feature either total or partial decoupling from the Discord platform.
- [ ] Custom stat tracking tool which will allow the tool to decouple from R6Analyst. This will allow greater control over the stats collected and likely allow us to minimize issues assosiated with the tool. This is for V1.0.0 [release].
 
# Bot Usage

Running the bot is fairly simple, and as of current it has 2 main functions:

 1) Uploading R6Analyst csv files for processing
 2) Viewing that data

In order to run any command for the bot you must @ the bot, it doesn't really matter where in your message you @ it, my convention is just it's the first part of the message (but doing it at the end or in the middle won't affect anything).

A command has successfully run if the bot deletes the message you sent to run the command and does not output an error. If the bot does not delete your message, and does not say anything then either you have encountered a bug (and I would appreciate you letting me know), or the bot is down. If it posts an error message (whether or not it deletes your message) an error has occurred. My DMs are always open if you encounter an error or bug. 

To upload a file to the bot, you use the =uploadfile command and attach the csv file to the message. The scrim, qual, or league portion of the command allows you to specify if the data in that csv should be bucketed under a scrim, a qual, or a league.
Usage: `@analyticsbot =uploadfile [scrim, qual, league]`
Example to upload a csv file which has data for a league match:
`@analyticsbot =uploadfile league <attached-file>`


To view data from the bot, you use the =playerstats command, and specify the uplay(s) (not case-sensitive) of the player(s) that you want to view stats for.
Usage: `@analyticsbot =playerstats <player_1> (<player_2> ... <player_n>)`
Example to view data for SpudsSack.MMG and Martyr.-
`@analyticsbot =playerstats Spudsack.MMG Martyr.-`


Finally, in case messages are cluttering, or you run into a few error, the bot also has a clear messages command, which will clear it's messages.
`@analyticsbot =clear` will clear the most recent message from the bot,
`@analyticsbot =clear error` will clear the 100 most recent error messages and,
`@analyticsbot =clear all` will clear the 100 most recent messages from the bot.