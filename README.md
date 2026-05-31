# Decision Recall

> 3개월 뒤의 너는, *왜* 그렇게 결정했는지 까먹는다.

## 이런 적 있어?

- 회사에서 "그때 왜 A 안 하고 B로 갔지?" — 결론은 기억나는데 *이유*는 사라짐
- 코드 리뷰에서 "이 패턴 안 쓰기로 했었는데... 왜였더라?"
- 친구가 똑같은 고민 들고 옴 — 작년에 똑같이 고민했는데 다시 처음부터
- 회의에서 같은 논의를 6개월 만에 또 함

결론은 살아남는데 **추론(reasoning)이 휘발**되니까, 같은 상황이 오면 처음부터 다시 풀게 됨.

## 이 도구가 하는 일

Claude Code 대화 중에 *진짜 결정*이 발생하는 순간, 한 줄로 박는다:

```
결정: 채용보류 | Q3 백엔드 채용 동결, 인프라 안정화 먼저
```

3주, 3개월 뒤 그 결정이 다시 도마 위에 오를 때:

```
/recall 채용
```

→ *왜* 그때 그렇게 결정했는지 그 자리에서 복기됨.

## 무엇이 아닌가

- 회의록 도구 X — 모든 걸 적는 게 아니라, **남길 가치 있는 것**만
- 일기 X — 감정 / 일상 X
- 생산성 트래커 X — 카운트 / 스트릭 X
- 코치 X — 너 결정이 옳았는지 안 말함

**기억 보조**일 뿐. 판단은 너가, 도구는 3개월 뒤에 그 판단을 *되돌려주는* 역할.

## 한 줄 형식

세 종류 마커, 한 줄에 하나:

```
결정: <짧은 토픽> | <한 줄 내용>
판단: <짧은 토픽> | <한 줄 내용>
원칙: <짧은 토픽> | <한 줄 내용>
```

| 마커 | 언제 쓰나 | 예시 |
|---|---|---|
| **결정** | A vs B 중 골랐을 때 | `결정: 이직고민 \| C사 제안 거절, 현 회사 1년 더 |
| **판단** | 비직관적 패턴/원인을 발견했을 때 | `판단: 매출하락 \| 신규 X 이탈이 원인, 기존 유지율은 정상` |
| **원칙** | 앞으로의 규칙을 세웠을 때 | `원칙: 회의 \| 30분 넘는 회의는 의제 사전 공유 의무` |

영어 별칭도 됨: `decision:` / `analysis:` / `principle:`

## 설치 (5분)

```bash
# 1. clone
git clone https://github.com/Nick-heo-eg/decision-recall.git ~/decision-recall

# 2. Claude Code 스킬 디렉토리에 연결
mkdir -p ~/.claude/skills ~/.claude/commands ~/.claude/agents
ln -s ~/decision-recall/.claude/skills/decision-recall ~/.claude/skills/decision-recall
ln -s ~/decision-recall/.claude/commands/recall.md ~/.claude/commands/recall.md
ln -s ~/decision-recall/.claude/commands/recall-search.md ~/.claude/commands/recall-search.md
ln -s ~/decision-recall/.claude/agents/decision-extractor.md ~/.claude/agents/decision-extractor.md
ln -s ~/decision-recall/.claude/agents/recall-viewer.md ~/.claude/agents/recall-viewer.md

# 3. Claude Code 재시작
```

확인: `/recall` 치면 "no trace yet, start using the skill" 나오면 OK.

## 처음 5분, 한번 돌려봐

→ [docs/quickstart.md](docs/quickstart.md) — 실제 일상 결정 1개로 끝까지 시뮬해보는 가이드.

자세한 설치/문제해결은 [docs/install_guide.md](docs/install_guide.md).

## 프라이버시

- 너의 trace는 **로컬 파일 1개**: `state/recall_trace.jsonl`
- `.gitignore`로 제외됨 — 절대 커밋 안 됨
- 이 스킬은 어떤 서버에도 전송 X
- 만든 사람도 너의 trace 못 봄
- 지우고 싶으면: `rm state/recall_trace.jsonl`

자세히: [docs/privacy.md](docs/privacy.md).

## License

MIT
