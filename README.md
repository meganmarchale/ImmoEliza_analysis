# ImmoEliza_analysis

## 🧹 Data Cleaning Summary

### General Cleaning

- Removed rows with missing essential values like `price` and `habitableSurface`.
- Dropped irrelevant or high-missing columns such as `floorCount`, `livingRoomSurface`, and `floodZoneType`.
- Cleaned inconsistent toilet/bathroom data:
  - Dropped rows with no bathroom and toilet info.
  - Assumed missing toilets are in the bathroom (toilet = 0).

### Missing Value Handling

- **Categorical**: Filled missing values with "unknown", "missing", or logical defaults.
  - EPC Score: Filled missing EPC ratings using the most common value per building condition, or "unknown".

```
buildingCondition
AS_NEW            B
GOOD              C
JUST_RENOVATED    B
TO_BE_DONE_UP     F
TO_RENOVATE       F
TO_RESTORE        F
```

- **Numeric**: Filled missing values with 0 where appropriate (e.g., parkingCountIndoor, facedeCount).

### Feature Added

- Created `region` column based on province (Flanders, Wallonia, Brussels).
- Simplified `terrace` into size categories (No terrace, Small, Medium, Big).
- Added `kitchen_installed` as a `True/False` indicator based on `kitchenSurface` and `kitchenType`.
