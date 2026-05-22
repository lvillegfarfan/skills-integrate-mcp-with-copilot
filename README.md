# Integrate MCP with Copilot

<img src="https://octodex.github.com/images/Professortocat_v2.png" align="right" height="200px" />

Hey lvillegfarfan!

Mona here. I'm done preparing your exercise. Hope you enjoy! 💚

Remember, it's self-paced so feel free to take a break! ☕️

## New Data Ingestion Pipeline

A data ingestion pipeline has been added under `scripts/` to extract document links from an Excel workbook, download DOCX/XLSX files, parse student tables, and aggregate the results into canonical JSON outputs.

Run the pipeline with:

```bash
python scripts/build_data.py --input data/example_links.xlsx --output data
```

The pipeline generates:

- `data/raw_activities.json`
- `data/students.json`
- `data/error_links.json`

---

&copy; 2025 GitHub &bull; [Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md) &bull; [MIT License](https://gh.io/mit)

