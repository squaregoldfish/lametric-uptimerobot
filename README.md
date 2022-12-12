# lametric-uptimerobot
Display UptimeRobot monitor status on LaMetric

## Description
This app for LaMetric displays counts of your UptimeRobot monitors. The counts are:
* Number of Up monitors (e.g. `7 ↑`). If all are up, displays `All ↑`.
* Number of Down montiors (e.g. `2 ↓`).
* Number of Paused monitors. (e.g. `3 ⏸`). Optional - see below.
* Number of Unknown monitors (e.g. `1 ???`). Usually displayed when a monitor has not been checked.

## Parameters
### UptimeRobot API Account Key
The app requires your API key to access your monitors. You can find it using the instructions below:
1. Log in to uptimerobot.com
1. Click `My Settings` at the top right of the screen
1. Scroll down to the `API Settings` section
1. Show your Main API Key
1. Copy the value into the option

### Ignore Paused Monitors
If this is selected, paused monitors are not shown by the app. For example, if you have 5 monitors and one is paused:

| Option       | Displays shown |
| ------------ | -------------- |
| Not selected | 4 Up, 1 Paused |
| Selected     | All Up         |
