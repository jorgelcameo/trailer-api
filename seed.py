import json
from pathlib import Path
from datetime import datetime
from database import SessionLocal, engine, Base
from models import Trailer as TrailerModel

Base.metadata.create_all(bind=engine)


def seed_trailers():
    db = SessionLocal()

    try:
        seed_file = Path(__file__).parent / "seeds" / "trailers.json"

        if not seed_file.exists():
            print(f"Seed file not found at {seed_file}")
            return

        print(f"Loading trailers from {seed_file}...")
        with open(seed_file, "r") as f:
            data = json.load(f)

        if "trailers" not in data:
            print("No trailers found in seed file")
            return

        trailers = data["trailers"]
        print(f"Found {len(trailers)} trailers in seed file")

        for trailer_data in trailers:
            external_id = trailer_data.get("id")

            if not external_id:
                print(f"Skipping trailer without id: {trailer_data.get('title')}")
                continue

            existing = db.query(TrailerModel).filter(
                TrailerModel.external_id == external_id
            ).first()

            if existing:
                print(f"Skipping existing trailer: {trailer_data.get('title')}")
                continue

            genres = ",".join(trailer_data.get("genres", [])) if trailer_data.get("genres") else None
            tags = ",".join(trailer_data.get("tags", [])) if trailer_data.get("tags") else None

            video_data = trailer_data.get("content", {}).get("videos", [{}])[0]

            # Parse release_date string to datetime object
            release_date = None
            release_date_str = trailer_data.get("releaseDate")
            if release_date_str:
                try:
                    release_date = datetime.strptime(release_date_str, "%Y-%m-%d")
                except (ValueError, TypeError):
                    print(f"Warning: Could not parse date '{release_date_str}' for {trailer_data.get('title')}")

            trailer = TrailerModel(
                external_id=external_id,
                title=trailer_data.get("title"),
                short_description=trailer_data.get("shortDescription"),
                long_description=trailer_data.get("longDescription"),
                video_url=video_data.get("url"),
                thumbnail_url=trailer_data.get("thumbnail"),
                release_date=release_date,
                duration=trailer_data.get("content", {}).get("duration"),
                genres=genres,
                tags=tags,
                video_type=video_data.get("videoType"),
                quality=video_data.get("quality"),
                language=trailer_data.get("content", {}).get("language"),
            )

            db.add(trailer)
            print(f"Added trailer: {trailer_data.get('title')}")

        db.commit()
        print("Database seeded successfully!")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_trailers()
