# ASVZ Bot Improvements - Less Detectable Version

## Summary of Changes

The bot has been modified to be **significantly less detectable** by checking for free places WITHOUT logging in first.

## Key Improvements

### 1. **Check Availability Before Login**
- **Before**: Bot logged in, then checked for free places repeatedly while authenticated
- **After**: Bot checks for free places on the public page, only logs in when spots are available

### 2. **Randomized Timing**
- **Before**: Fixed 30-second intervals (obvious automation pattern)
- **After**: Random intervals between 25-90 seconds (appears more human-like)

### 3. **Reduced Authentication Footprint**
- **Before**: Continuous logged-in session for hours/days
- **After**: Only authenticate when actually enrolling

## Modified Code Sections

### File: `src/asvz_bot.py`

**Line ~400**: Main enrollment flow now checks WITHOUT login first
```python
logging.info("Checking for available places (WITHOUT logging in).")
self.__wait_for_free_places(driver)  # This runs on public page
logging.info("Lesson has free places - now logging in to enroll")
self.__organisation_login(driver)  # Only login when spots available
```

**Line ~664-695**: Updated `__wait_for_free_places()` method
- Added randomized retry intervals (25-90 seconds)
- Added better logging
- Reloads public page after failed enrollment attempt

## Benefits

### ✅ Much Less Detectable
- No logged-in session sitting idle
- Only authenticates when necessary
- Random timing appears more human

### ✅ Reduced Server Load
- Viewing public pages is lighter than authenticated sessions
- Better citizenship on ASVZ infrastructure

### ✅ Lower Risk
- Authentication logs only show login when actually enrolling
- Pattern looks like: "user checked page, saw free spot, logged in, enrolled"
- Not: "user was logged in for 48 hours straight refreshing constantly"

## How It Works Now

```
┌─────────────────────────────────────────┐
│ 1. Load lesson page (no login)         │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 2. Check "Freie Plätze" counter         │
└──────────────┬──────────────────────────┘
               │
               ▼
         ┌─────┴─────┐
         │           │
    NO SPOTS      SPOTS AVAILABLE
         │           │
         ▼           ▼
   ┌──────────┐  ┌──────────────┐
   │ Wait     │  │ Login NOW    │
   │ 25-90s   │  │ Enroll       │
   │ Refresh  │  │ Success!     │
   └────┬─────┘  └──────────────┘
        │
        └──► Loop back to step 2
```

## Testing the Changes

### Test locally:
```bash
cd C:\Users\mflori\Desktop\asvz-bot\src
.venv\Scripts\activate
python asvz_bot.py lesson YOUR_LESSON_ID
```

Watch the logs - you should see:
```
INFO: Enrollment is already open. Checking for available places (WITHOUT logging in).
INFO: Lesson is booked out. Rechecking in 47 secs..
INFO: Lesson is booked out. Rechecking in 62 secs..
INFO: Found 1 free place(s)!
INFO: Lesson has free places - now logging in to enroll
INFO: Login to 'ETH Zürich'
```

## Deployment to Cloud

The improved version works perfectly on cloud VMs. Use the updated `run_bot.sh` script.

### Recommended cron schedule (every 2 hours):
```cron
0 */2 * * * /home/ubuntu/asvz-bot/run_bot.sh
```

### For more aggressive monitoring (every 30 minutes):
```cron
*/30 * * * * /home/ubuntu/asvz-bot/run_bot.sh
```

## Important Reminders

⚠️ **This bot was discontinued due to ASVZ Fair Play Rules**

Even with these improvements:
- You're still using automation (against policy)
- ASVZ can still detect patterns if they look
- Use responsibly and at your own risk

### Recommendations:
- Don't run continuously for weeks
- Use conservative check intervals (2-4 hours, not 30 seconds)
- Consider manual checking instead
- Respect ASVZ's Fair Play guidelines

## What's Still Detectable

Even with improvements, ASVZ could still detect:
- Same IP address checking repeatedly
- You log in right after checking (timing correlation)
- Browser fingerprinting (Selenium can be detected)
- Pattern of always checking at exact intervals

This is **better** but not **invisible**.
