import os
import re
from pathlib import Path

def analyze_and_cleanup():
    """
    ✅ Analyzes existing batches
    ✅ Identifies empty/corrupted files
    ✅ Cleans them up
    ✅ Determines restart point
    """
    raw_dir = Path("data/raw")
    
    if not raw_dir.exists():
        print("[❌] data/raw directory not found!")
        return
    
    print("\n" + "="*70)
    print("🔍 VANDOR'S BATCH ANALYSIS & CLEANUP")
    print("="*70 + "\n")
    
    # Analyze all batch files
    batch_files = sorted(raw_dir.glob("generated_*.txt"))
    
    if not batch_files:
        print("[❌] No batch files found!")
        return
    
    good_batches = []
    bad_batches = []
    empty_batches = []
    
    for batch_file in batch_files:
        try:
            with open(batch_file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read().strip()
                lines = [l for l in content.split("\n") if l.strip()]
            
            # Extract batch number
            match = re.search(r"generated_(\d+)\.txt", batch_file.name)
            batch_num = int(match.group(1)) if match else 0
            word_count = len(lines)
            
            # Quality control
            if word_count == 0:
                empty_batches.append(batch_num)
                print(f"  [❌] Batch {batch_num:03d}: EMPTY ({word_count} words)")
            elif word_count < 5000:
                bad_batches.append(batch_num)
                print(f"  [⚠️] Batch {batch_num:03d}: CORRUPTED ({word_count} words)")
            elif word_count >= 9500:  # Nearly 10k
                good_batches.append(batch_num)
                print(f"  [✅] Batch {batch_num:03d}: GOOD ({word_count} words)")
            else:
                bad_batches.append(batch_num)
                print(f"  [⚠️] Batch {batch_num:03d}: CORRUPTED ({word_count} words)")
        
        except Exception as e:
            match = re.search(r"generated_(\d+)\.txt", batch_file.name)
            batch_num = int(match.group(1)) if match else 0
            bad_batches.append(batch_num)
            print(f"  [❌] Batch {batch_num:03d}: ERROR ({e})")
    
    print("\n" + "="*70)
    print(f"📊 RESULTS:")
    print("="*70)
    print(f"  ✅ GOOD BATCHES: {len(good_batches)} ({good_batches[0]}-{good_batches[-1] if good_batches else 'N/A'})")
    print(f"  ⚠️ CORRUPTED BATCHES: {len(bad_batches)}")
    print(f"  ❌ EMPTY BATCHES: {len(empty_batches)}")
    
    # Cleanup plan
    to_delete = sorted(set(empty_batches + bad_batches))
    
    if to_delete:
        print(f"\n🗑️ BATCHES TO DELETE: {len(to_delete)} files")
        print(f"   {to_delete[:10]}{'...' if len(to_delete) > 10 else ''}")
        
        print(f"\n⚠️ Confirm deletion? (y/n): ", end="")
        
        # Auto-confirm for CI/CD
        response = "y"
        print(response)
        
        if response.lower() == "y":
            for batch_num in to_delete:
                file_path = raw_dir / f"generated_{batch_num:03d}.txt"
                try:
                    file_path.unlink()
                    print(f"  ✅ Deleted: generated_{batch_num:03d}.txt")
                except Exception as e:
                    print(f"  [❌] Failed to delete: generated_{batch_num:03d}.txt ({e})")
            
            print(f"\n[✅] Cleanup completed!")
    
    # Determine restart point
    remaining_good = [b for b in good_batches if b not in to_delete]
    
    if remaining_good:
        next_batch = max(remaining_good) + 1
        print(f"\n🚀 RESTART POINT:")
        print(f"   Start from batch {next_batch:03d}!")
        print(f"   (Previous good batches preserved)")
    else:
        next_batch = 1
        print(f"\n🚀 RESTART POINT:")
        print(f"   Start from batch 1 (clean start)")
    
    print("\n" + "="*70)
    return next_batch

def show_statistics():
    """Display current word pool statistics"""
    raw_dir = Path("data/raw")
    
    total_words = 0
    total_files = 0
    
    for batch_file in raw_dir.glob("generated_*.txt"):
        try:
            with open(batch_file, "r", encoding="utf-8", errors="ignore") as f:
                lines = [l for l in f.read().strip().split("\n") if l.strip() and ":" in l]
                total_words += len(lines)
                total_files += 1
        except:
            pass
    
    print(f"\n📈 OVERALL STATISTICS:")
    print(f"   File count: {total_files}")
    print(f"   Word count: {total_words:,}")
    print(f"   Remaining target: {1_000_000 - total_words:,}")
    print()

if __name__ == "__main__":
    next_batch = analyze_and_cleanup()
    show_statistics()
    
    print(f"""
💡 NEXT STEPS:
    1. Replace src/generator.py with generator_v2.py
    2. Run GitHub workflow
    3. Bot will automatically start from batch {next_batch:03d}
    """)

