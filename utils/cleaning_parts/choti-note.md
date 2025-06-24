## EPC score

fill according to `buildingCondition`

```
buildingCondition
AS_NEW            B
GOOD              C
JUST_RENOVATED    B
TO_BE_DONE_UP     F
TO_RENOVATE       F
TO_RESTORE        F
```

with `unknown` buildingCondition fill with epcScore `unknown`

## buildingCondition

- fill NA with unknown

## toiletCount

- if no info for both bathroom + toilet : drop rows.
- If toilet count > 0 but no bathroom count : drop rows.
- If missing toilet value - assume that toilet in the bathroom — value = 0

## floorCount, livingRoomSurface , floodZoneType
