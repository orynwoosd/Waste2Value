import argparse
import asyncio

from sqlalchemy import func, select

from database import AsyncSessionLocal, engine
from models import User
from schemas import UserRole


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Promote one existing user to the initial site owner."
    )
    identifier = parser.add_mutually_exclusive_group(required=True)
    identifier.add_argument("--email")
    identifier.add_argument("--phone")
    parser.add_argument(
        "--confirm-owner",
        action="store_true",
        help="Confirm that this is the intended owner account.",
    )
    return parser.parse_args()


async def bootstrap_owner(args: argparse.Namespace) -> None:
    if not args.confirm_owner:
        raise SystemExit("Re-run with --confirm-owner after checking the account.")

    async with AsyncSessionLocal() as db:
        existing_owner = await db.scalar(
            select(User.id).where(User.role == UserRole.MEGA_USER)
        )
        if existing_owner is not None:
            raise SystemExit(
                "An owner already exists. Use the protected admin workflow instead."
            )

        identifier = args.email if args.email is not None else args.phone
        field = User.email if args.email is not None else User.phonenumber
        user = await db.scalar(
            select(User).where(func.lower(field) == identifier.lower())
        )
        if user is None:
            raise SystemExit("No user was found. Register the owner account first.")

        user.role = UserRole.MEGA_USER
        await db.commit()
        print(f"Promoted user {user.id} ({user.email}) to MEGA_USER.")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(bootstrap_owner(parse_args()))