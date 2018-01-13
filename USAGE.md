# 상세 설정

Open Dccon Selector는 트위치 대시보드의 '확장' 항목에서 Open Dccon Selector의 우측 하단 톱니바퀴 아이콘을 클릭하여
설정할 수 있습니다.

## 1. Dccon URL

Dccon URL은 방송에서 사용하는 디시콘 데이터를 가져오기 위한 URL입니다.

이 값은 반드시 Open Dccon Selector에서 지원하는 형식의 데이터에 대한 URL이어야 합니다.

더 자세한 사항은 [지원하는 Dccon type](#21-지원하는-dccon-type)을 참고하세요.

## 2. Dccon Type

Dccon Type은 Dccon URL에서 제공하는 디시콘 데이터의 형식을 지정합니다.

Dccon URL에서 제공하는 디시콘 데이터의 형식과 Dccon Type 값이 다를 경우 정상적으로 Open Dccon Selector가 동작하지
않습니다.

### 2.1. 지원하는 Dccon type

#### 2.1.1. Open Dccon Format

Open Dccon Format은 [JSAssist Open DCcon](https://github.com/rishubil/jsassist-open-dccon)에서 사용하는 디시콘 데이터
형식이며, Open Dccon Selector의 기본 Dccon type이기도 합니다.

예시: [https://rishubil.github.io/jsassist-open-dccon/static/dccon_list.json](https://rishubil.github.io/jsassist-open-dccon/static/dccon_list.json)

#### 2.1.2. Open Dccon Format (Relative path)

Open Dccon Format (Relative path)는 기본적으로 Open Dccon Format과 동일하지만, `path` 값의 URL이 절대 경로가 아닌
상대 경로인 형식입니다.

#### 2.1.3. Funzinnu Dccon Format

Funzinnu Dccon Format은 [Funzinnu](https://www.twitch.tv/funzinnu)님이 사용하시는 디시콘 형식입니다.

예시: [http://funzinnu.cafe24.com/stream/dccon.php](http://funzinnu.cafe24.com/stream/dccon.php)

#### 2.1.4. Telk Dccon Format

Telk Dccon Format은 [텔크](https://www.twitch.tv/telk5093)님이 사용하시는 디시콘 형식입니다.

예시: [http://tv.telk.kr/?mode=json](http://tv.telk.kr/?mode=json)

## 3. Cache Dccon data to server

이 옵션이 활셩화되어 있을 경우 디시콘 데이터를 Open Dccon Selector 서버에 캐시하여 제공합니다.

(디시콘 이미지 파일은 캐시하지 않습니다.)

Open Dccon Format을 제외한 모든 Dccon type에 대하여 해당 옵션을 비활성화 할 수 없습니다.

## 3.1. Open Dccon Format을 제외한 모든 Dccon type에 대하여 해당 옵션을 비활성화 할 수 없는 이유?

기본적으로 Open Dccon Selector는 Open Dccon Format을 제외한 모든 Dccon type은 내부 처리를 통해 Open Dccon Format으로
변환하여 사용합니다.

그러나 디시콘 데이터는 자주 변경되지 않으므로 이를 매 요청마다 변환하는 것은 비효율적이므로, Open Dccon Format을
제외한 모든 Dccon type에 대한 데이터는 캐싱된 데이터만을 제공하고 있습니다.

# 4. Test data format

해당 기능은 입력한 Dccon URL과 Dccon Type의 값을 통해 디시콘 데이터에 접근 가능한지 확인합니다.

# 5. Updated cached Dccon data

해당 기능은 입력한 디시콘 데이터를 다시 캐싱합니다.

저장되지 않은 설정 값에 대해서는 동작하지 않으므로, 설정을 변경했을 경우 설정 내용을 저장한 후 사용해야 합니다.

'Cache Dccon data to server' 옵션이 비활성화되어 있을 경우 사용할 수 없습니다.
