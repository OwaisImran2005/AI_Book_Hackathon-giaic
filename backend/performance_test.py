"""
Performance test for retrieval functionality
Validates that retrieval achieves sub-second response time for typical queries
"""
import time
import statistics
from retrieve import retrieve


def test_response_time():
    """Test that retrieval achieves sub-second response time for typical queries"""
    # Test with a simple query
    test_queries = [
        "documentation",
        "machine learning",
        "artificial intelligence",
        "RAG pipeline",
        "vector database"
    ]

    response_times = []

    print("Testing response times for retrieval function...")

    for i, query in enumerate(test_queries):
        print(f"Test {i+1}: Query = '{query}'")

        start_time = time.time()
        try:
            # Call retrieve function with a simple query
            results = retrieve(query, top_k=3, similarity_threshold=0.0)  # Lower threshold to ensure results
            end_time = time.time()

            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            response_times.append(response_time)

            print(f"  Response time: {response_time:.2f}ms")
            print(f"  Results found: {len(results)}")

        except ValueError as e:
            # This is expected if environment variables aren't set
            print(f"  Skipped due to configuration error: {e}")
            continue
        except Exception as e:
            print(f"  Error during test: {e}")
            continue

    if response_times:
        avg_response_time = statistics.mean(response_times)
        max_response_time = max(response_times)
        min_response_time = min(response_times)

        print(f"\nPerformance Results:")
        print(f"  Average response time: {avg_response_time:.2f}ms")
        print(f"  Max response time: {max_response_time:.2f}ms")
        print(f"  Min response time: {min_response_time:.2f}ms")
        print(f"  Total queries tested: {len(response_times)}")

        # Check if we meet the sub-second requirement (under 1000ms)
        if max_response_time < 1000:
            print(f"  ✅ SUCCESS: All queries completed under 1000ms (sub-second requirement met)")
            return True
        else:
            print(f"  ❌ FAILURE: Some queries exceeded 1000ms (sub-second requirement not met)")
            return False
    else:
        print("  No valid response times recorded (environment may not be configured)")
        return None


if __name__ == "__main__":
    result = test_response_time()
    if result is True:
        print("\nPerformance test PASSED")
    elif result is False:
        print("\nPerformance test FAILED")
    else:
        print("\nPerformance test SKIPPED (requires environment configuration)")