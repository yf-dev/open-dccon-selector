# Open Dccon Selector

[한국어](/README.ko.md)

Open Dccon Selector is a Twitch overlay extension for Streamers that support Dccon chat.
By using Open Dccon Selector, viewers can find and use Dccons through overlay.

## Video Tutorial

You can watch the video tutorial by clicking thumbnail below.

[![Introduction and setup guide of Open Dccon Selector](https://img.youtube.com/vi/JQbwyMTIUwg/0.jpg)](https://www.youtube.com/watch?v=JQbwyMTIUwg "Introduction and setup guide of Open Dccon Selector")

## What is Dccon chat?

Dccon chat is a feature that displays a small image on a video chat screen with a chat message, such as a KakaoTalk
emoticons and a telegram sticker.
Dccon Chat can be used by typing specific keywords of each Dccon starting with `~` characters in the chat window
like `~hello`.

Streamers can always add/remove/modify Dccon, which viewers can use in their broadcasts, so Dccon chat is a good way
to show the personality of each broadcast.

## How to apply Dccon chat to broadcast

Currently, you can use [JSAssist Open DCcon](https://github.com/rishubil/jsassist-open-dccon),
[Bridge BBCC](https://github.com/krynen/BridgeBBCC),
[ChatAssistX-Client](https://github.com/Lastorder-DC/ChatAssistX-Client) which are open source.

For how to apply each program, refer to the program guide.

- JSAssist Open DCcon: [https://github.com/rishubil/jsassist-open-dccon](https://github.com/rishubil/jsassist-open-dccon)
- Bridge BBCC: [https://github.com/krynen/BridgeBBCC](https://github.com/krynen/BridgeBBCC)
- ChatAssistX-Client: [https://github.com/Lastorder-DC/ChatAssistX-Client](https://github.com/Lastorder-DC/ChatAssistX-Client)

## Why Open Dccon Selector?

Each streamer has a different Dccon for chatting, so each streamer gives viewers a list of Dccons available on their
broadcasts on a separate website.

Examples:
- [Funzinnu](https://www.twitch.tv/funzinnu)
  - [http://funzinnu.com/dccon.html](http://funzinnu.com/dccon.html)
- [Yeokka](https://www.twitch.tv/yeokka)
  - [https://krynen.github.io/jsassist-custom-css/list.html](https://krynen.github.io/jsassist-custom-css/list.html)
- [Telk](https://www.twitch.tv/telk5093)
  - [http://tv.telk.kr/list](http://tv.telk.kr/list)

However, it is very troublesome to find Dccon on a separate website during the broadcast and use it back to broadcast.
(Especially, it is more inconvenient when you are watching the broadcast on full screen.)

So I created an Open Dccon Selector to use Dccon chat quickly without leaving the current viewing screen.

## How to apply Open Dccon Selector to broadcasts

First, go to the URL below.

[https://dashboard.twitch.tv/extensions/iotylqfktkxdjwyk1gdq2rlc7kw7zo](https://dashboard.twitch.tv/extensions/iotylqfktkxdjwyk1gdq2rlc7kw7zo)

Click on the 'Install' button in the upper right corner and click 'Configure' button to set Dccon chat data.

In the extension configuration, enter the URL of your Dccon chat data in the Dccon URL field and click the 'Submit'
button.

(Example of Dccon chat data - `https://rishubil.github.io/jsassist-open-dccon/static/dccon_list.json`)

Now You can go to the "Extensions" section of the Twitch dashboard and activate the Open Dccon Selector.

For more detailed settings, see [configuration document](/CONFIG.md).

## License

MIT

