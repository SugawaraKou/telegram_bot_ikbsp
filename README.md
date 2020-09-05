# telegram_bot_ikbsp

This page can be read on its own to find the code snippet you need right now. 

It is also a follow-up to the page [Introduction to the API](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Introduction-to-the-API). If you come from there, you can leave your command line open and just try out a few of these snippets.

- [Pure API](#pure-api)
    + [Fetch updates](#fetch-updates)
    + [Fetch images sent to your Bot](#fetch-images-sent-to-your-bot)
    + [Reply to messages](#reply-to-messages)
- [General code snippets](#general-code-snippets)
    + [Post a text message](#post-a-text-message)
    + [Reply to a message](#reply-to-a-message)
    + [Send a chat action](#send-a-chat-action)
    + [Requesting location and contact from user](#requesting-location-and-contact-from-user)
  * [Message Formatting (bold, italic, code, ...)](#message-formatting-bold-italic-code-)
    + [Post a text message with Markdown formatting](#post-a-text-message-with-markdown-formatting)
    + [Post a text message with HTML formatting](#post-a-text-message-with-html-formatting)
    + [Message entities](#message-entities)
    + [Telegram formatting to BBCode](#telegram-formatting-to-bbcode)
  * [Working with files and media](#working-with-files-and-media)
    + [Post an image file from disk](#post-an-image-file-from-disk)
    + [Post a voice file from disk](#post-a-voice-file-from-disk)
    + [Post a photo from a URL](#post-a-photo-from-a-url)
    + [Post an audio from disk](#post-an-audio-from-disk)
    + [Post a file from disk](#post-a-file-from-disk)
    + [Post an image from memory](#post-an-image-from-memory)
    + [Post a media group from a URL](#post-a-media-group-from-a-url)
    + [Get image with dimensions closest to a desired size](#get-image-with-dimensions-closest-to-a-desired-size)
    + [Download a file](#download-a-file)
  * [Keyboard Menus](#keyboard-menus)
    + [Custom Keyboards](#custom-keyboards)
    + [Remove a custom keyboard](#remove-a-custom-keyboard)
  * [Other useful stuff](#other-useful-stuff)
    + [Generate flag emojis from country codes](#generate-flag-emojis-from-country-codes)
    + [Get the add group message](#get-the-add-group-message)
    + [Exclude forwarded channel posts in discussion groups from MessageHandlers](#exclude-forwarded-channel-posts-in-discussion-groups-from-messagehandlers)
- [Advanced snippets](#advanced-snippets)
    + [Restrict access to a handler (decorator)](#restrict-access-to-a-handler-decorator)
      - [Usage](#usage)
    + [Send action while handling command (decorator)](#send-action-while-handling-command-decorator)
      - [Usage](#usage-1)
    + [Build a menu with Buttons](#build-a-menu-with-buttons)
      - [Usage](#usage-2)
    + [Cached Telegram group administrator check](#cached-telegram-group-administrator-check)
    + [Simple way of restarting the bot](#simple-way-of-restarting-the-bot)
    + [Store ConversationHandler States](#store-conversationhandler-states)
      - [Usage](#usage-3)
    + [Save and load jobs using pickle](#save-and-load-jobs-using-pickle)
    + [An (good) error handler](#an-good-error-handler)
- [What to read next?](#what-to-read-next)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>



## Pure API

#### Fetch updates
To fetch messages sent to your Bot, you can use the [getUpdates](https://core.telegram.org/bots/api#getupdates) API method.

**Note:** You don't have to use `get_updates` if you are writing your bot with the `telegram.ext` submodule, since `telegram.ext.Updater` takes care of fetching all updates for you. Read more about that [here](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot).

```python
updates = bot.get_updates()
print([u.message.text for u in updates])
```

#### Fetch images sent to your Bot

```python
updates = bot.get_updates()
print([u.message.photo for u in updates if u.message.photo])
```

#### Reply to messages
You'll always need the `chat_id`

```python
chat_id = bot.get_updates()[-1].message.chat_id
```

## General code snippets
These snippets usually apply to both ways of fetching updates. If you're using `telegram.ext`, you can get the `chat_id` in your handler callback with `update.message.chat_id`.

**Note:** In general, you can send messages to users by passing their user id as the `chat_id`. 
If the bot has a chat with the user, it will send the message to that chat.



#### Post a text message
[ᵀᴱᴸᴱᴳᴿᴬᴹ](https://core.telegram.org/bots/api#sendmessage)

```python
bot.send_message(chat_id=chat_id, text="I'm sorry Dave I'm afraid I can't do that.")
```

**Note:** `send_message` method (as any of `send_*` methods of `Bot` class) returns the instance of `Message` class, so it can be used in code later.

#### Reply to a message

This is a shortcut to `bot.send_message` with sane defaults. Read more about it [in the docs](http://python-telegram-bot.readthedocs.io/en/latest/telegram.html#telegram.Message.reply_text). 

```python
update.message.reply_text("I'm sorry Dave I'm afraid I can't do that.")
```

**Note:** There are equivalents of this method for replying with photos, audio etc., and similar shortcuts exist throughout the library. Related PRs: [#362](https://github.com/python-telegram-bot/python-telegram-bot/pull/362), [#420](https://github.com/python-telegram-bot/python-telegram-bot/pull/420), [#423](https://github.com/python-telegram-bot/python-telegram-bot/pull/423)

#### Send a chat action
[ᵀᴱᴸᴱᴳᴿᴬᴹ](https://core.telegram.org/bots/api#sendchataction)
Use this to tell the user that something is happening on the bot's side:

```python
bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
```
Alternatively, if you have several commands and don't want to repeat the above code snippet inside all commands, you can copy the snippet below and just decorate the callback functions with `@send_typing_action`.

```python
from functools import wraps

def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func

@send_typing_action
def my_handler(update, context):
    pass # Will send 'typing' action while processing the request.
```

#### Requesting location and contact from user

```python
location_keyboard = telegram.KeyboardButton(text="send_location", request_location=True)
contact_keyboard = telegram.KeyboardButton(text="send_contact", request_contact=True)
custom_keyboard = [[ location_keyboard, contact_keyboard ]]
reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
bot.send_message(chat_id=chat_id, 
...                  text="Would you mind sharing your location and contact with me?", 
...                  reply_markup=reply_markup)
```

### Message Formatting (bold, italic, code, ...)

#### Post a text message with Markdown formatting
[ᵀᴱᴸᴱᴳᴿᴬᴹ](https://core.telegram.org/bots/api#sendmessage)

*Note:* In the API 4.5 update, Telegram introduced MarkdownV2, which supports nested entities and needs other escaping than v1. Markdown V1 is refered as legacy mode the the official API docs and you should prefer MarkdownV2. Make sure to also use `reply_markdown_v2` instead of `reply_markdown` etc.

```python
bot.send_message(chat_id=chat_id, 
                 text="*bold* _italic_ `fixed width font` [link](http://google.com)\.", 
                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
```

#### Post a text message with HTML formatting
[ᵀᴱᴸᴱᴳᴿᴬᴹ](https://core.telegram.org/bots/api#sendmessage)

```python
bot.send_message(chat_id=chat_id, 
                 text='<b>bold</b> <i>italic</i> <a href="http://google.com">link</a>.', 
                 parse_mode=telegram.ParseMode.HTML)
```

#### Message entities
[ᵀᴱᴸᴱᴳᴿᴬᴹ](https://core.telegram.org/bots/api#messageentity)
To use MessageEntity, extract the entities and their respective text from a Message object using `parse_entities`.  

**Note:** This method should always be used instead of the ``entities`` attribute, since it calculates the correct substring from the message text based on UTF-16 codepoints - that is, it extracts the correct string even on when working with weird characters such as Emojis.

```python
entities = message.parse_entities()
```

#### Telegram formatting to BBCode
This is an example how to use entities to convert Telegram formatting to BBCode. In the current version it does *not* support nested entities.

Define parsing function:
```python
import sys

def parse_bbcode(message_text, entities, urled=False):
    """BBCode parsing function"""
    if message_text is None:
        return None

    if not sys.maxunicode == 0xffff:
        message_text = message_text.encode('utf-16-le')

    bbcode_text = ''
    last_offset = 0

    for entity, text in sorted(entities.items(), key=(lambda item: item[0].offset)):

        if entity.type == 'text_link':
            insert = '[url={}]{}[/url]'.format(entity.url, text)
        elif entity.type == 'mention':
            insert = '[url=https://t.me/{0}]{1}[/url]'.format(text.strip('@'),text)
        elif entity.type == 'url' and urled:
            insert = '[url={0}]{0}[/url]'.format(text)
        elif entity.type == 'bold':
            insert = '[b]' + text + '[/b]'
        elif entity.type == 'italic':
            insert = '[i]' + text + '[/i]'
        elif entity.type == 'underline':
            insert = '[u]' + text + '[/u]'
        elif entity.type == 'strikethrough':
            insert = '[s]' + text + '[/s]'
        elif entity.type == 'code':
            insert = '[code]' + text + '[/code]'
        elif entity.type == 'pre':
            insert = '[pre]' + text + '[/pre]'
        else:
            insert = text
        if sys.maxunicode == 0xffff:
            bbcode_text += message_text[last_offset:entity.offset] + insert
        else:
            bbcode_text += message_text[last_offset * 2:entity.offset * 2].decode('utf-16-le') + insert

        last_offset = entity.offset + entity.length

    if sys.maxunicode == 0xffff:
        bbcode_text += message_text[last_offset:]
    else:
        bbcode_text += message_text[last_offset * 2:].decode('utf-16-le')
    return bbcode_text
```
Call it with:
```python
entities = update.message.parse_entities()
bbcode = parse_bbcode(update.message.text, entities, urled=True)
```

...or for photo captions:
```python
entities = update.message.parse_caption_entities()
bbcode = parse_bbcode(caption, entities, urled=True)
```
`bbcode` will contain message/caption text formatted in BBCode. `urled` parameter determines if URLs in text are to be processed as links or left as text.

There are many more API methods. To read the full API documentation, visit the [Telegram API documentation](https://core.telegram.org/bots/api) or the [library documentation of telegram.Bot](http://python-telegram-bot.readthedocs.io/en/latest/telegram.bot.html)

### Working with files and media

#### Post an image file from disk
[ᵀᴱᴸᴱᴳᴿᴬᴹ](https://core.telegram.org/bots/api#sendphoto)

```python
bot.send_photo(chat_id=chat_id, photo=open('tests/test.png', 'rb'))
```

#### Post a voice file from disk
[ᵀᴱᴸᴱᴳᴿᴬᴹ](https://core.telegram.org/bots/api#sendvoice)

```python
bot.send_voice(chat_id=chat_id, voice=open('tests/telegram.ogg', 'rb'))
```

#### Post a photo from a URL
[ᵀᴱᴸᴱᴳᴿᴬᴹ](https://core.telegram.org/bots/api#sendphoto)

```python
bot.send_photo(chat_id=chat_id, photo='https://telegram.org/img/t_logo.png')
```

#### Post a gif from a URL (send_animation)
[ᵀᴱᴸᴱᴳᴿᴬᴹ](https://core.telegram.org/bots/api#sendanimation)

```python
bot.send_animation(chat_id, animation, duration=None, width=None, height=None, thumb=None, caption=None, parse_mode=None, disable_notification=False, reply_to_message_id=None, reply_markup=None, timeout=20, **kwargs)
```
See the [online documentation](https://python-telegram-bot.readthedocs.io/en/latest/telegram.bot.html#telegram.Bot.send_animation)

#### Post a media group from a URL
[ᵀᴱᴸᴱᴳᴿᴬᴹ](https://core.telegram.org/bots/api#sendmediagroup)

```python
from telegram import InputMediaPhoto

list_of_urls = [
    'https://upload.wikimedia.org/wikipedia/commons/c/c7/Gigantic_galapagos_turtle_on_the_island_of_santa_cruz.JPG',
    'https://upload.wikimedia.org/wikipedia/commons/9/99/T.h._hermanni_con_speroni_5.JPG',
    'https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Sheldonbasking.JPG/1280px-Sheldonbasking.JPG' 
]

media_group = list()

for number, url in enumerate(list_of_urls):
    media_group.append(InputMediaPhoto(media=url), caption="Turtle" + number)

bot.send_media_group(chat_id=chat_id, media=media_group)
```
See the [online documentation](https://python-telegram-bot.readthedocs.io/en/latest/telegram.bot.html#telegram.Bot.send_media_group)

#### Post an audio from disk
[ᵀᴱᴸᴱᴳᴿᴬᴹ](https://core.telegram.org/bots/api#sendaudio)

```python
bot.send_audio(chat_id=chat_id, audio=open('tests/test.mp3', 'rb'))
```

#### Post a file from disk
[ᵀᴱᴸᴱᴳᴿᴬᴹ](https://core.telegram.org/bots/api#senddocument)

```python
bot.send_document(chat_id=chat_id, document=open('tests/test.zip', 'rb'))
```

#### Post an image from memory
In this example, `image` is a PIL (or Pillow) `Image` object, but it works the same with all media types.

```python
from io import BytesIO
bio = BytesIO()
bio.name = 'image.jpeg'
image.save(bio, 'JPEG')
bio.seek(0)
bot.send_photo(chat_id, photo=bio)
```

#### Get image with dimensions closest to a desired size
Where `photos` is a list of `PhotoSize` objects and `desired_size` is a tuple containing the desired size.

```python
def get_closest(photos, desired_size):
    def diff(p): return p.width - desired_size[0], p.height - desired_size[1]
    def norm(t): return abs(t[0] + t[1] * 1j)
    return min(photos, key=lambda p:  norm(diff(p)))
```

#### Download a file
[ᵀᴱᴸᴱᴳᴿᴬᴹ](https://core.telegram.org/bots/api#getfile)

```python
file_id = message.voice.file_id
newFile = bot.get_file(file_id)
newFile.download('voice.ogg')
```

**Note:** For downloading photos, keep in mind that `update.message.photo` is an array of different photo sizes. Use `update.message.photo[-1]` to get the biggest size.

### Keyboard Menus

#### Custom Keyboards
[ᵀᴱᴸᴱᴳᴿᴬᴹ](https://core.telegram.org/bots#keyboards)

```python
custom_keyboard = [['top-left', 'top-right'], 
                   ['bottom-left', 'bottom-right']]
reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
bot.send_message(chat_id=chat_id, 
                 text="Custom Keyboard Test", 
                 reply_markup=reply_markup)
```

See also: [Build a menu with Buttons](#build-a-menu-with-buttons)


#### Remove a custom keyboard

```python
reply_markup = telegram.ReplyKeyboardRemove()
bot.send_message(chat_id=chat_id, text="I'm back.", reply_markup=reply_markup)
```

### Other useful stuff

#### Generate flag emojis from country codes

The Unicode flag emoji for any country can by definition be calculated from the countries [2 letter country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2). The following snippet only works in Python 3.

```python
OFFSET = 127462 - ord('A')

def flag(code):
    code = code.upper()
    return chr(ord(code[0]) + OFFSET) + chr(ord(code[1]) + OFFSET)

>>> flag('de')
'🇩🇪'
>>> flag('us')
'🇺🇸'
>>> flag('ru')
'🇷🇺'
```

#### Get the add group message
```python
def add_group(update, context):
    for member in update.message.new_chat_members:
        update.message.reply_text("{username} add group".format(username=member.username))

add_group_handle = MessageHandler(Filters.status_update.new_chat_members, add_group)
dispatcher.add_handler(add_group_handle)
```

#### Exclude forwarded channel posts in discussion groups from MessageHandlers	
If you're using MessageHandlers and do not want them to respond to the channel posts automatically forwarded to the discussion group linked to your channel, you can use this filter in your MessageHandler:	
```python	
~ Filters.user(777000)
```	
`777000` is the user id of the Telegram Service Messages chat, that also gives you your login codes and in this case will be the originator of the forwarded channel post.

## Advanced snippets

#### Restrict access to a handler (decorator)

<!--- The extraction of the user_id is going to be built in on python-telegram-bot version 6.0.
TODO: Upon release, update this snippet!--->

This decorator allows you to restrict the access of a handler to only the `user_ids` specified in `LIST_OF_ADMINS`.

```python
from functools import wraps

LIST_OF_ADMINS = [12345678, 87654321]

def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            print("Unauthorized access denied for {}.".format(user_id))
            return
        return func(update, context, *args, **kwargs)
    return wrapped
```

##### Usage

Add a `@restricted` decorator on top of your handler declaration:

```python
@restricted
def my_handler(update, context):
    pass  # only accessible if `user_id` is in `LIST_OF_ADMINS`.
```
---

#### Send action while handling command (decorator)
This parametrized decorator allows you to signal different actions depending on the type of response of your bot. This way users will have similar feedback from your bot as they would from a real human. 
```python
from functools import wraps

def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(update, context,  *args, **kwargs)
        return command_func
    
    return decorator
```

##### Usage
![Result](https://i.imgur.com/ErBKSS4.png)

You can decorate handler callbacks directly with `@send_action(ChatAction.<Action>)` or create aliases and decorate with them (more readable) .
```python
send_typing_action = send_action(ChatAction.TYPING)
send_upload_video_action = send_action(ChatAction.UPLOAD_VIDEO)
send_upload_photo_action = send_action(ChatAction.UPLOAD_PHOTO)
```
With the above aliases, the following decorators are equivalent
```python
@send_typing_action
def my_handler(update, context):
    pass  # user will see 'typing' while your bot is handling the request.
    
@send_action(ChatAction.TYPING)
def my_handler(update, context):
    pass  # user will see 'typing' while your bot is handling the request.
```
All possible actions are documented [here](https://core.telegram.org/bots/api#sendchataction).

---



#### Build a menu with Buttons

Often times you will find yourself in need for a menu with dynamic content. Use the following `build_menu` method to create a button layout with `n_cols` columns out of a list of `buttons`.

```python
def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu
```

You can use the `header_buttons` and `footer_buttons` lists to put buttons in the first or last row respectively.

##### Usage

![Output](http://i.imgur.com/susvvR7.png)

Replace the `...` in below snippet by an appropriate argument, as indicated in the [InlineKeyboardButton documentation](https://python-telegram-bot.readthedocs.io/en/latest/telegram.inlinekeyboardbutton.html). If you want to use `KeyboardButtons`, use `ReplyKeyboardMarkup` instead of `InlineKeyboardMarkup`.

```python
button_list = [
    InlineKeyboardButton("col1", callback_data=...),
    InlineKeyboardButton("col2", callback_data=...),
    InlineKeyboardButton("row 2", callback_data=...)
]
reply_markup = InlineKeyboardMarkup(util.build_menu(button_list, n_cols=2))
bot.send_message(..., "A two-column menu", reply_markup=reply_markup)
```

Or, if you need a dynamic version, use list comprehension to generate your `button_list` dynamically from a list of strings:

```python
some_strings = ["col1", "col2", "row2"]
button_list = [[KeyboardButton(s)] for s in some_strings]
```

This is especially useful if put inside a helper method like `get_data_buttons` to work on dynamic data and updating the menu according to user input.

To handle the `callback_data`, you need to set a `CallbackQueryHandler`.

#### Cached Telegram group administrator check
If you want to limit certain bot functions to group administrators, you have to test if a user is an administrator in the group in question. This however requires an extra API request, which is why it can make sense to cache this information for a certain time, especially if your bot is very busy.

This snippet requires [this timeout-based cache decorator](http://code.activestate.com/recipes/325905-memoize-decorator-with-timeout/#c1). ([gist mirror](https://gist.github.com/jh0ker/56f5b4fb7d015b1b9e4c74d4a91d4568))

Save the decorator to a new file named `mwt.py` and add this line to your imports:
```python
from mwt import MWT
```

Then, add the following decorated function to your script. You can change the timeout as required.
```python
@MWT(timeout=60*60)
def get_admin_ids(bot, chat_id):
    """Returns a list of admin IDs for a given chat. Results are cached for 1 hour."""
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]
```

You can then use the function like this:
```python
if update.effective_user.id in get_admin_ids(context.bot, update.message.chat_id):
    # admin only
```

**Note:** Private chats and groups with `all_members_are_administrator` flag, are not covered by this snippet. Make sure you handle them.



#### Simple way of restarting the bot

The following example allows you to restart the bot from within a handler. It goes without saying that you should protect this method from access by unauthorized users, which is why we are using a `Filters.user` filter. If you want multiple users to have access the restart command, you can pass a list of usernames as well. You can also filter by user IDs which is arguably a bit safer since they can't change. See the [docs](https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.filters.html#telegram.ext.filters.Filters.user) for more information.

This example is using closures so it has access to the `updater` variable. Alternatively, you could make it global.

```python
import os
import sys
from threading import Thread

# Other code

def main():
    updater = Updater("TOKEN", use_context=True)
    dp = updater.dispatcher

    # Add your other handlers here...

    def stop_and_restart():
        """Gracefully stop the Updater and replace the current process with a new one"""
        updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def restart(update, context):
        update.message.reply_text('Bot is restarting...')
        Thread(target=stop_and_restart).start()

    # ...or here...

    dp.add_handler(CommandHandler('r', restart, filters=Filters.user(username='@jh0ker')))

    # ...or here, depending on your preference :)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
```

#### Store ConversationHandler States

Version 12 and up includes tools for [making your bot persistent](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Making-your-bot-persistent).

#### Save and load jobs using pickle
The following snippet pickles the jobs in the job queue periodically and on bot shutdown, and unpickles and queues them again on startup. Since pickle doesn't support threading primitives, therefore their values and states are extracted (this information may change in the future, always check the `Job` documentation).

**Note:** `Job` is not yet safe for threads so eventually some special condition may occur. In a previous example, the content of `Job` was modified which resulted in some asynchronous processing errors; now the content of `Job` is extracted without modifying it which is much more safe.

```python
import pickle
from time import time
from datetime import timedelta

from telegram.ext import Updater, Job


JOBS_PICKLE = 'job_tuples.pickle'

# WARNING: This information may change in future versions (changes are planned)
JOB_DATA = ('callback', 'interval', 'repeat', 'context', 'days', 'name', 'tzinfo')
JOB_STATE = ('_remove', '_enabled')


def load_jobs(jq):
    with open(JOBS_PICKLE, 'rb') as fp:
        while True:
            try:
                next_t, data, state = pickle.load(fp)
            except EOFError:
                break  # loaded all jobs

            # New object with the same data
            job = Job(**{var: val for var, val in zip(JOB_DATA, data)})

            # Restore the state it had
            for var, val in zip(JOB_STATE, state):
                attribute = getattr(job, var)
                getattr(attribute, 'set' if val else 'clear')()

            job.job_queue = jq

            next_t -= time()  # convert from absolute to relative time

            jq._put(job, next_t)


def save_jobs(jq):
    with jq._queue.mutex:  # in case job_queue makes a change

        if jq:
            job_tuples = jq._queue.queue
        else:
            job_tuples = []

        with open(JOBS_PICKLE, 'wb') as fp:
            for next_t, job in job_tuples:

                # This job is always created at the start
                if job.name == 'save_jobs_job':
                    continue

                # Threading primitives are not pickleable
                data = tuple(getattr(job, var) for var in JOB_DATA)
                state = tuple(getattr(job, var).is_set() for var in JOB_STATE)

                # Pickle the job
                pickle.dump((next_t, data, state), fp)


def save_jobs_job(context):
    save_jobs(context.job_queue)


def main():
    # updater = Updater(...)

    job_queue = updater.job_queue

    # Periodically save jobs
    job_queue.run_repeating(save_jobs_job, timedelta(minutes=1))

    try:
        load_jobs(job_queue)

    except FileNotFoundError:
        # First run
        pass

    # updater.start_[polling|webhook]()
    # updater.idle()

    # Run again after bot has been properly shutdown
    save_jobs(job_queue)


if __name__ == '__main__':
    main()
```

#### An (good) error handler
The following snippet is an example of an error handler. It notifies the user when an error happens and notifies the dev(s) of the error, including the traceback and where it happend. The comments in the code try to explain exactly what happens when and why, so editing it to fit your special needs should be a breeze.

```python
from telegram import ParseMode
from telegram.utils.helpers import mention_html
import sys
import traceback

# this is a general error handler function. If you need more information about specific type of update, add it to the
# payload in the respective if clause
def error(update, context):
    # add all the dev user_ids in this list. You can also add ids of channels or groups.
    devs = [208589966]
    # we want to notify the user of this problem. This will always work, but not notify users if the update is an 
    # callback or inline query, or a poll update. In case you want this, keep in mind that sending the message 
    # could fail
    if update.effective_message:
        text = "Hey. I'm sorry to inform you that an error happened while I tried to handle your update. " \
               "My developer(s) will be notified."
        update.effective_message.reply_text(text)
    # This traceback is created with accessing the traceback object from the sys.exc_info, which is returned as the
    # third value of the returned tuple. Then we use the traceback.format_tb to get the traceback as a string, which
    # for a weird reason separates the line breaks in a list, but keeps the linebreaks itself. So just joining an
    # empty string works fine.
    trace = "".join(traceback.format_tb(sys.exc_info()[2]))
    # lets try to get as much information from the telegram update as possible
    payload = ""
    # normally, we always have an user. If not, its either a channel or a poll update.
    if update.effective_user:
        payload += f' with the user {mention_html(update.effective_user.id, update.effective_user.first_name)}'
    # there are more situations when you don't get a chat
    if update.effective_chat:
        payload += f' within the chat <i>{update.effective_chat.title}</i>'
        if update.effective_chat.username:
            payload += f' (@{update.effective_chat.username})'
    # but only one where you have an empty payload by now: A poll (buuuh)
    if update.poll:
        payload += f' with the poll id {update.poll.id}.'
    # lets put this in a "well" formatted text
    text = f"Hey.\n The error <code>{context.error}</code> happened{payload}. The full traceback:\n\n<code>{trace}" \
           f"</code>"
    # and send it to the dev(s)
    for dev_id in devs:
        context.bot.send_message(dev_id, text, parse_mode=ParseMode.HTML)
    # we raise the error again, so the logger module catches it. If you don't use the logger module, use it.
    raise
``` 

## What to read next?
If you haven't read the tutorial "[Extensions – Your first Bot](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-–-Your-first-Bot)" yet, you might want to do it now.
