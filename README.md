# Twitter DogBot

The code for https://twitter.com/DogBot42

Because one dog per day keeps the doctor away.

Thanks to https://twitter.com/TwitterDev/status/1621026986784337922 the bot is now posting also on [telegram](https://t.me/one_dog_per_day) and [mastodon](https://hostux.social/@aloissiola).

## Deployment

- Create a Dog Api key [here](https://thedogapi.com/)
- Create a [Twitter Developer Account](https://developer.twitter.com/en/portal/dashboard)
- Create an `env.json` file with the dog api, the twitter key and the twitter secret.
- Run `python authenticate.py` and follow instructions.
- Add `twitter_token_key` and `twitter_token_secret` to the env.json
- Add script e.g. to crontab: 

```
0 12 * * * cd ~/dogbottwitter && flock -n /tmp/dogbottwitter.lockfile python3 main.py
```