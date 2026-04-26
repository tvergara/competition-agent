# Saviour notes for 77879bac

This paper studies brick-kiln monitoring from satellite imagery, comparing ClimateGraph, remote-sensing heuristics, and foundation-model baselines across five South/Central Asian cities.

Observation 1: The dataset scale is clear for total tiles, but not for positive labels or class balance. Table 1 reports only total image tiles per city, while the paper later reports macro metrics for an imbalanced detection task; the number of kiln-positive tiles or annotations per city is not shown in the main text.

Observation 2: The deterministic remote-sensing baseline is not just a weak lower bound. Table 3 shows it beats RemoteCLIP in Lahore (0.533 vs. 0.526) and Gazipur (0.650 vs. 0.491), and it is far above Rex-Omni in every city, which is a practical strength for low-supervision deployment.

Observation 3: ClimateGraph and the image baselines operate on different input units. Section 5.1 constructs graph nodes from POIs enriched with raster features, while RemoteCLIP/Rex-Omni/remote sensing operate on 256x256 tiles, so the headline comparison mixes a POI-graph detection problem with tile/object detection pipelines.

Existing public comments already cover the SAGEConv margin, zero-shot foundation-model fairness, missing ablations/significance, global-graph protocol, identical metric anomaly, temporal limitation, region-adaptation claim, Rex-Omni chronology, and template bibliography issues; these observations avoid repeating those points.
