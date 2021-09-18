App is hosted on Heroku free tier [here](https://album2library.herokuapp.com/)

## Huh?
I'm still a bit salty at spotify for removing the "feature" where when you like an album, it automatically likes each song in the album and hence they appear in your liked songs.

So I made this app to like all your songs from albums that you've liked, but not liked the individual songs.

## _A word of warning_
I didn't bother making this reversable, so you should be sure you want this. For me it introduced 2k new songs to my library.

### _Another warning_
If your Spotify library is too chunky and cause the process to take more than 30 seconds, Heroku free tier will fall over and give you a 500 (I think).
I don't wanna try fix that so I wrote [a cli version](https://github.com/ashtonmoomoo/spotify-utils-cli) where you can supply your own API keys and run the process locally if you're _that_ keen.
