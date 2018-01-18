# Open Dccon Selector

[English](/README.md)

Open Dccon Selector는 디시콘 채팅을 지원하는 스트리머를 위한 오버레이 확장 프로그램입니다.
사용 가능한 디시콘을 오버레이를 통해 빠르게 찾아 사용할 수 있습니다.

## 디시콘 채팅이란?

디시콘 채팅은 카카오톡의 이모티콘이나 텔레그렘의 스티커와 같이 채팅 메시지와 함께 작은 이미지를 채팅 화면에 표시하는
기능입니다.
디시콘 채팅은 `~안녕`과 같이 `~` 문자로 시작하는 각 디시콘의 특정 키워드를 채팅창에 입력하여 사용할 수 있습니다.

스트리머는 자신의 방송에서 사용할 수 있는 디시콘을 언제나 마음대로 추가/삭제/수정할 수 있으므로, 디시콘 채팅은 각
방송의 개성을 나타내기 위한 좋은 수단이기도 합니다.

## 디시콘 채팅을 방송에 적용하는 법

현재는 오픈소스로 공개된 [JSAssist Open DCcon](https://github.com/rishubil/jsassist-open-dccon),
[Bridge BBCC](https://github.com/krynen/BridgeBBCC),
[ChatAssistX-Client](https://github.com/Lastorder-DC/ChatAssistX-Client)를 사용할 수 있습니다.

각 프로그램의 적용 방법은 해당 프로그램의 가이드를 참고하세요.

- JSAssist Open DCcon: [https://github.com/rishubil/jsassist-open-dccon](https://github.com/rishubil/jsassist-open-dccon)
- Bridge BBCC: [https://github.com/krynen/BridgeBBCC](https://github.com/krynen/BridgeBBCC)
- ChatAssistX-Client: [https://github.com/Lastorder-DC/ChatAssistX-Client](https://github.com/Lastorder-DC/ChatAssistX-Client)

## Open Dccon Selector를 만든 이유

스트리머마다 사용 가능한 디시콘의 종류가 다르므로, 각 스트리머는 자신의 방송에서 사용 가능한 디시콘의 목록을 별도의
웹 사이트로 구성하여 시청자에게 제공하고 있습니다.

예시:
- [Funzinnu](https://www.twitch.tv/funzinnu)
  - [http://funzinnu.com/dccon.html](http://funzinnu.com/dccon.html)
- [Yeokka](https://www.twitch.tv/yeokka)
  - [https://krynen.github.io/jsassist-custom-css/list.html](https://krynen.github.io/jsassist-custom-css/list.html)
- [텔크](https://www.twitch.tv/telk5093)
  - [http://tv.telk.kr/list](http://tv.telk.kr/list)

그러나 방송 시청 중 별도의 웹 사이트에 접속하여 디시콘을 찾고, 이를 다시 방송 채팅 화면에 붙여넣어 사용하는 것은
번거로운 일입니다.
(특히 전체 화면으로 방송을 보고 있을 때에는 더욱 불편합니다.)

따라서 현재 시청중인 방송 화면에서 벗어나지 않고 빠르게 디시콘 채팅을 사용하기 위해 Open Dccon Selector를
제작했습니다.

## 방송에 Open Dccon Selector를 적용하는 방법

먼저, 아래의 주소에 접속합니다.

[https://www.twitch.tv/ext/q9hjbqg3j6ukrq81pqyb9j5kwomzl8-0.0.1](https://www.twitch.tv/ext/q9hjbqg3j6ukrq81pqyb9j5kwomzl8-0.0.1)

우측 상단의 '설치' 버튼을 클릭하고, 디시콘 채팅 데이터를 설정하기 위해 '구성' 버튼을 클릭하여 확장 프로그램
구성으로 진입합니다.

확장 프로그램 구성에서 Dccon Url 입력란에 사용중인 디시콘 채팅 데이터 주소를 입력하고 'Submit' 버튼을 클릭합니다.

(디시콘 채팅 데이터 예시 - `https://rishubil.github.io/jsassist-open-dccon/static/dccon_list.json`)

이제 트위치 대시보드의 '확장' 항목으로 이동하여 에서 Open Dccon Selector를 '활성화' 하여 바로 사용할 수 있습니다.

더 자세한 설정은 [상세 설정](/CONFIG.ko.md)을 참고하세요.

## License

MIT

