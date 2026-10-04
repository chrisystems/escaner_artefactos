#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

DEFAULT_EXTENSIONS = ["jar", "war", "ear", "zip"]


def parse_extensions(value: str):
    return [ext.strip().lower() for ext in value.split(",") if ext.strip()]


def find_artifacts(root: Path, extensions):
    extensions = set(extensions)
    matches = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower().lstrip(".") in extensions:
            matches.append(path)
    return matches


def build_summary(input_dir: Path, artifacts, args):
    relative_paths = [str(path.relative_to(input_dir)) for path in artifacts]
    summary = {
        "input_dir": str(input_dir),
        "artifacts_found": len(artifacts),
        "artifacts": relative_paths,
        "jobs": args.jobs,
        "extensiones": parse_extensions(args.extensiones),
        "escanear_terceros": args.escanear_terceros,
        "pii": args.pii,
        "reanudar": args.reanudar,
        "grupos_internos": args.grupos_internos,
        "omitir_grupos": args.omitir_grupos,
    }
    return summary


def main():
    parser = argparse.ArgumentParser(
        description="Escáner de artefactos para identificar archivos empaquetados y posibles riesgos."
    )
    parser.add_argument("-d", "--dir", dest="directorio", required=True, help="Directorio a escanear")
    parser.add_argument("-o", "--out", dest="salida", required=True, help="Directorio de salida")
    parser.add_argument("-j", "--jobs", type=int, default=8, help="Número de procesos concurrentes")
    parser.add_argument(
        "--extensiones",
        default="jar,war,ear,zip",
        help="Extensiones a revisar separadas por comas",
    )
    parser.add_argument("--escanear-terceros", action="store_true", help="Analizar librerías de terceros")
    parser.add_argument("--pii", action="store_true", help="Buscar datos personales")
    parser.add_argument("--reanudar", action="store_true", help="Agregar artefactos nuevos sin reprocesar lo anterior")
    parser.add_argument("--grupos-internos", default="", help="Filtro de grupos internos")
    parser.add_argument("--omitir-grupos", default="", help="Grupos a omitir")
    args = parser.parse_args()

    input_dir = Path(args.directorio)
    if not input_dir.exists():
        parser.error(f"El directorio indicado no existe: {input_dir}")

    ext = parse_extensions(args.extensiones) or DEFAULT_EXTENSIONS
    artifacts = find_artifacts(input_dir, ext)

    out_dir = Path(args.salida)
    out_dir.mkdir(parents=True, exist_ok=True)

    summary = build_summary(input_dir, artifacts, args)
    summary_path = out_dir / "resumen.md"
    summary_path.write_text(
        "# Resumen del escaneo\n\n"
        + f"- Directorio de entrada: `{input_dir}`\n"
        + f"- Artefactos encontrados: {summary['artifacts_found']}\n"
        + f"- Extensiones revisadas: {', '.join(summary['extensiones'])}\n"
        + f"- Jobs: {args.jobs}\n"
        + ("- Escaneo de terceros: activado\n" if args.escanear_terceros else "- Escaneo de terceros: desactivado\n")
        + ("- PII: activado\n" if args.pii else "- PII: desactivado\n")
        + ("- Reanudar: activado\n" if args.reanudar else "- Reanudar: desactivado\n")
        + "\n## Ficheros\n"
        + ("\n".join(f"- `{path}`" for path in summary["artifacts"]) if summary["artifacts"] else "- No se encontraron artefactos coincidentes."),
        encoding="utf-8",
    )

    (out_dir / "reporte.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Se encontraron {len(artifacts)} artefactos en {input_dir}")
    print(f"Resumen guardado en {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
