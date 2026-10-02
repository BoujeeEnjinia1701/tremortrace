# BOM notes

Every line in `bom/bom.csv` is priced (TRL 3). The parts total is USD 43.69 per band, checked by `docs/04-calcs/sizing.py`. Value-engineering target: USD 150 (`budget_usd` in `project.yaml`, a hypothetical control target, not a limit); the estimate is USD 106.31 under it. TRT-DDR-003 (design for construction) changed lines 2, 4, 5, 7, 8, 9 and 11: four countersunk lid screws in place of two, the cell plug removed, ribs and a glue collar in the base, foam pads and epoxy in the consumables. Item 1 is a woven textile strap of about 8 g, which replaced the 12 g silicone strap under TRT-DDR-002 to restore mass margin under R6. Item numbers 1 to 8 match the exploded view and drawing TRT-DWG-002.

The LiPo cell price, size and mass were checked against the Adafruit product 1317 listing on 2026-09-25. Other prices are indicative and are confirmed at order. Suppliers are named where a specific part is intended; otherwise a supplier type is given.
