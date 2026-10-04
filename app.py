
import streamlit as st
import streamlit.components.v1 as components
import json
import html

st.set_page_config(
    page_title="Sorty & Hoppy's Sorting Garden",
    page_icon="🐧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# Global styles
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@500;600;700;800;900&family=Pacifico&display=swap');

:root {
    --pink-1: #fff8fc;
    --pink-2: #ffeaf5;
    --pink-3: #ffd6ea;
    --pink-4: #ffb9d9;
    --pink-5: #ff8fc2;
    --ink: #5d4760;
    --purple: #8f70a0;
    --white: #ffffff;
}

html, body, [class*="css"] {
    font-family: "Nunito", sans-serif;
    color: var(--ink);
}

.stApp {
    background:
        radial-gradient(circle at 15% 20%, rgba(255,255,255,.95) 0 90px, transparent 91px),
        radial-gradient(circle at 85% 10%, rgba(255,255,255,.75) 0 70px, transparent 71px),
        linear-gradient(145deg, #fff8fc 0%, #ffeefa 45%, #fffdfd 100%);
}

.block-container {
    max-width: 1180px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #6d4f72 !important;
}

.cute-title {
    font-family: "Pacifico", cursive;
    font-size: clamp(2.4rem, 5vw, 4.3rem);
    text-align: center;
    color: #ff79b1;
    text-shadow: 0 3px 0 rgba(255,255,255,.85);
    margin-bottom: .2rem;
}

.subtitle {
    text-align: center;
    color: #8f728f;
    font-size: 1.08rem;
    margin-bottom: 1.3rem;
}

.hero-card, .soft-card, .concept-card, .tip-card {
    background: rgba(255,255,255,.88);
    border: 2px solid #ffd9eb;
    border-radius: 28px;
    box-shadow: 0 12px 30px rgba(205, 130, 167, .12);
}

.hero-card {
    padding: 1.1rem 1.3rem;
    text-align: center;
    margin: .8rem 0 1.4rem;
}

.soft-card, .concept-card, .tip-card {
    padding: 1rem 1.2rem;
    margin: .45rem 0 .8rem;
}

.mascots {
    font-size: 3rem;
    letter-spacing: .55rem;
}

.stButton > button {
    width: 100%;
    border-radius: 18px !important;
    border: 2px solid #ffd1e6 !important;
    background: linear-gradient(180deg, #ffffff 0%, #fff0f7 100%) !important;
    color: #6b4d70 !important;
    font-weight: 800 !important;
    min-height: 3.2rem;
    box-shadow: 0 6px 15px rgba(255, 145, 190, .12);
    transition: all .18s ease;
}
.stButton > button:hover {
    transform: translateY(-2px) scale(1.01);
    border-color: #ff9cc9 !important;
    color: #ff6faa !important;
}

div[data-testid="stCode"] {
    border-radius: 20px;
    border: 2px solid #ffe0ef;
    overflow: hidden;
}

[data-testid="stExpander"] {
    border: 2px solid #ffe0ef !important;
    border-radius: 18px !important;
    background: rgba(255,255,255,.8);
}

[data-testid="stTextInput"] input {
    border-radius: 16px;
    border: 2px solid #ffd8ea;
    background: #fffdfd;
}

.pill {
    display:inline-block;
    padding:.32rem .72rem;
    margin:.18rem .25rem .18rem 0;
    background:#fff;
    border:1.6px solid #ffd5e8;
    border-radius:999px;
    color:#7b627f;
    font-weight:800;
    font-size:.9rem;
}

.footer {
    text-align:center;
    margin-top:2rem;
    color:#a184a3;
    font-size:.9rem;
}
</style>
""", unsafe_allow_html=True)

ALGORITHMS = [
    "Selection Sort",
    "Bubble Sort",
    "Insertion Sort",
    "Merge Sort",
    "Quick Sort",
    "Recursive Bubble Sort",
    "Recursive Insertion Sort",
    "Arrays",
]

ALGO_EMOJI = {
    "Selection Sort": "🔎",
    "Bubble Sort": "🫧",
    "Insertion Sort": "🧩",
    "Merge Sort": "🧁",
    "Quick Sort": "⚡",
    "Recursive Bubble Sort": "🫧🔁",
    "Recursive Insertion Sort": "🧩🔁",
    "Arrays": "🥕",
}

CONCEPTS = {
    "Selection Sort": {
        "one_liner": "Find the smallest item and place it in the next correct position.",
        "story": "🐧 Sorty looks through the unsorted part, finds the tiniest number, and 🐰 Hoppy swaps it into the front. Then they repeat for the remaining part.",
        "steps": [
            "Start at index 0.",
            "Search the rest of the array for the smallest value.",
            "Swap that smallest value with the value at the current index.",
            "Move one position right and repeat.",
        ],
        "complexity": ("O(n²)", "O(1)", "No"),
    },
    "Bubble Sort": {
        "one_liner": "Compare neighbors and swap them when they are in the wrong order.",
        "story": "🫧 Big numbers bubble to the right. 🐧 Sorty compares two neighbors, and 🐰 Hoppy swaps them if the left one is bigger.",
        "steps": [
            "Compare index 0 and 1.",
            "Swap if the left value is bigger.",
            "Continue with the next neighboring pair.",
            "After one pass, the largest unsorted value reaches the end.",
        ],
        "complexity": ("O(n²)", "O(1)", "Yes"),
    },
    "Insertion Sort": {
        "one_liner": "Take one item and insert it into the correct place in the sorted left side.",
        "story": "🐰 Hoppy picks one card. 🐧 Sorty slides bigger cards to the right until the picked card has a cozy correct spot.",
        "steps": [
            "Treat the first element as already sorted.",
            "Pick the next element as the key.",
            "Shift larger elements one place to the right.",
            "Insert the key into the gap.",
        ],
        "complexity": ("O(n²)", "O(1)", "Yes"),
    },
    "Merge Sort": {
        "one_liner": "Split the array into tiny pieces, sort them, then merge them back together.",
        "story": "🐧 Sorty keeps splitting the line into smaller groups. 🐰 Hoppy carefully merges the groups in increasing order.",
        "steps": [
            "Split the array into left and right halves.",
            "Recursively sort both halves.",
            "Compare the front values of both halves.",
            "Take the smaller one and build the merged result.",
        ],
        "complexity": ("O(n log n)", "O(n)", "Yes"),
    },
    "Quick Sort": {
        "one_liner": "Choose a pivot, put smaller values left and larger values right, then repeat.",
        "story": "⚡ 🐧 Sorty chooses a pivot. 🐰 Hoppy moves smaller numbers before it and bigger numbers after it, then they do the same inside each side.",
        "steps": [
            "Choose a pivot (this site uses the last element).",
            "Move values smaller than or equal to the pivot to the left.",
            "Place the pivot in its final position.",
            "Recursively quick-sort the left and right parts.",
        ],
        "complexity": ("O(n log n) average, O(n²) worst", "O(log n) average recursion", "Usually No"),
    },
    "Recursive Bubble Sort": {
        "one_liner": "Bubble once, then recursively bubble the smaller remaining part.",
        "story": "🫧🐧 One pass sends the largest value to the end. Then Sorty calls the same idea again for one fewer element.",
        "steps": [
            "Make one bubble-sort pass across the first n elements.",
            "The largest value reaches position n - 1.",
            "Call the same function for n - 1 elements.",
            "Stop when n becomes 1.",
        ],
        "complexity": ("O(n²)", "O(n) recursion stack", "Yes"),
    },
    "Recursive Insertion Sort": {
        "one_liner": "Recursively sort the first n-1 elements, then insert the last one correctly.",
        "story": "🧩🐰 First, Hoppy asks the smaller prefix to sort itself. Then 🐧 Sorty inserts the last card into the right place.",
        "steps": [
            "Recursively sort the first n - 1 values.",
            "Save the last value as the key.",
            "Shift bigger sorted values to the right.",
            "Insert the key.",
        ],
        "complexity": ("O(n²)", "O(n) recursion stack", "Yes"),
    },
}

JAVA_CODE = {
"Selection Sort": """public class SelectionSort {
    public static void selectionSort(int[] arr) {
        int n = arr.length;

        for (int i = 0; i < n - 1; i++) {
            int minIndex = i;

            for (int j = i + 1; j < n; j++) {
                if (arr[j] < arr[minIndex]) {
                    minIndex = j;
                }
            }

            int temp = arr[i];
            arr[i] = arr[minIndex];
            arr[minIndex] = temp;
        }
    }
}""",
"Bubble Sort": """public class BubbleSort {
    public static void bubbleSort(int[] arr) {
        int n = arr.length;

        for (int i = 0; i < n - 1; i++) {
            boolean swapped = false;

            for (int j = 0; j < n - 1 - i; j++) {
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                    swapped = true;
                }
            }

            if (!swapped) {
                break;
            }
        }
    }
}""",
"Insertion Sort": """public class InsertionSort {
    public static void insertionSort(int[] arr) {
        for (int i = 1; i < arr.length; i++) {
            int key = arr[i];
            int j = i - 1;

            while (j >= 0 && arr[j] > key) {
                arr[j + 1] = arr[j];
                j--;
            }

            arr[j + 1] = key;
        }
    }
}""",
"Merge Sort": """public class MergeSort {
    public static void mergeSort(int[] arr, int left, int right) {
        if (left >= right) return;

        int mid = left + (right - left) / 2;

        mergeSort(arr, left, mid);
        mergeSort(arr, mid + 1, right);
        merge(arr, left, mid, right);
    }

    private static void merge(int[] arr, int left, int mid, int right) {
        int[] temp = new int[right - left + 1];
        int i = left;
        int j = mid + 1;
        int k = 0;

        while (i <= mid && j <= right) {
            if (arr[i] <= arr[j]) {
                temp[k++] = arr[i++];
            } else {
                temp[k++] = arr[j++];
            }
        }

        while (i <= mid) temp[k++] = arr[i++];
        while (j <= right) temp[k++] = arr[j++];

        for (int x = 0; x < temp.length; x++) {
            arr[left + x] = temp[x];
        }
    }
}""",
"Quick Sort": """public class QuickSort {
    public static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pivotIndex = partition(arr, low, high);

            quickSort(arr, low, pivotIndex - 1);
            quickSort(arr, pivotIndex + 1, high);
        }
    }

    private static int partition(int[] arr, int low, int high) {
        int pivot = arr[high];
        int i = low - 1;

        for (int j = low; j < high; j++) {
            if (arr[j] <= pivot) {
                i++;

                int temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }

        int temp = arr[i + 1];
        arr[i + 1] = arr[high];
        arr[high] = temp;

        return i + 1;
    }
}""",
"Recursive Bubble Sort": """public class RecursiveBubbleSort {
    public static void recursiveBubbleSort(int[] arr, int n) {
        if (n == 1) {
            return;
        }

        for (int i = 0; i < n - 1; i++) {
            if (arr[i] > arr[i + 1]) {
                int temp = arr[i];
                arr[i] = arr[i + 1];
                arr[i + 1] = temp;
            }
        }

        recursiveBubbleSort(arr, n - 1);
    }
}""",
"Recursive Insertion Sort": """public class RecursiveInsertionSort {
    public static void recursiveInsertionSort(int[] arr, int n) {
        if (n <= 1) {
            return;
        }

        recursiveInsertionSort(arr, n - 1);

        int key = arr[n - 1];
        int j = n - 2;

        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }

        arr[j + 1] = key;
    }
}""",
}

LINE_EXPLANATIONS = {
"Selection Sort": [
    ("int n = arr.length;", "Remember how many values are in the array."),
    ("for (int i = 0; i < n - 1; i++)", "Pick the next position that needs the correct smallest value."),
    ("int minIndex = i;", "For now, assume the current position contains the smallest value."),
    ("for (int j = i + 1; j < n; j++)", "Search every value to the right."),
    ("if (arr[j] < arr[minIndex])", "If we discover something smaller..."),
    ("minIndex = j;", "Remember where that new smallest value lives."),
    ("swap", "Swap the smallest value into position i."),
],
"Bubble Sort": [
    ("for (int i = 0; i < n - 1; i++)", "Repeat several passes through the array."),
    ("boolean swapped = false;", "Remember whether this pass actually changed anything."),
    ("for (int j = 0; j < n - 1 - i; j++)", "Walk through only the unsorted part."),
    ("if (arr[j] > arr[j + 1])", "If two neighbors are backwards..."),
    ("swap", "Swap the neighbors."),
    ("swapped = true;", "Mark that the array changed."),
    ("if (!swapped) break;", "No swap means the array is already sorted, so stop early."),
],
"Insertion Sort": [
    ("for (int i = 1; i < arr.length; i++)", "Start from the second value; the first is already a sorted group of one."),
    ("int key = arr[i];", "Pick up the value we want to insert."),
    ("int j = i - 1;", "Look just left of the key."),
    ("while (j >= 0 && arr[j] > key)", "Keep moving while the left value is too large."),
    ("arr[j + 1] = arr[j];", "Slide that large value one spot right."),
    ("j--;", "Look farther left."),
    ("arr[j + 1] = key;", "Drop the key into the gap."),
],
"Merge Sort": [
    ("if (left >= right) return;", "A piece with 0 or 1 value is already sorted."),
    ("int mid = ...;", "Find the middle point."),
    ("mergeSort(arr, left, mid);", "Sort the left half recursively."),
    ("mergeSort(arr, mid + 1, right);", "Sort the right half recursively."),
    ("merge(...);", "Combine both sorted halves."),
    ("if (arr[i] <= arr[j])", "Compare the front values of the two halves."),
    ("temp[k++] = ...;", "Copy the smaller value into the temporary sorted array."),
    ("arr[left + x] = temp[x];", "Copy the merged result back to the original array."),
],
"Quick Sort": [
    ("if (low < high)", "Only work when this section contains at least two values."),
    ("int pivotIndex = partition(...);", "Partition the section and get the pivot's final index."),
    ("quickSort(...left...);", "Recursively sort everything left of the pivot."),
    ("quickSort(...right...);", "Recursively sort everything right of the pivot."),
    ("int pivot = arr[high];", "Use the last value as the pivot."),
    ("if (arr[j] <= pivot)", "Values small enough belong on the left side."),
    ("swap arr[i] and arr[j]", "Grow the 'small values' zone."),
    ("return i + 1;", "Return the pivot's final index."),
],
"Recursive Bubble Sort": [
    ("if (n == 1) return;", "Base case: one value is automatically sorted."),
    ("for (int i = 0; i < n - 1; i++)", "Bubble through the current unsorted prefix."),
    ("if (arr[i] > arr[i + 1])", "Swap neighbors that are backwards."),
    ("recursiveBubbleSort(arr, n - 1);", "Largest value is fixed at the end, so recurse on one fewer value."),
],
"Recursive Insertion Sort": [
    ("if (n <= 1) return;", "Base case: one value is already sorted."),
    ("recursiveInsertionSort(arr, n - 1);", "First sort the first n - 1 values."),
    ("int key = arr[n - 1];", "Pick the last value as the key to insert."),
    ("int j = n - 2;", "Start comparing from the end of the sorted prefix."),
    ("while (j >= 0 && arr[j] > key)", "Shift every value that is bigger than the key."),
    ("arr[j + 1] = key;", "Insert the key into its final gap."),
],
}

def parse_array(raw):
    try:
        nums = [int(x.strip()) for x in raw.split(",") if x.strip() != ""]
    except ValueError:
        return None
    if len(nums) < 2 or len(nums) > 9:
        return None
    return nums

def add_step(steps, arr, active=None, message="", action="look"):
    steps.append({
        "arr": arr.copy(),
        "active": active or [],
        "message": message,
        "action": action
    })

def selection_steps(arr):
    a = arr.copy(); s = []
    add_step(s, a, [], "Ready! Sorty will hunt for the smallest number. 🐧", "start")
    n = len(a)
    for i in range(n - 1):
        m = i
        add_step(s, a, [i], f"Position {i}: begin the tiny-number hunt.", "look")
        for j in range(i + 1, n):
            add_step(s, a, [m, j], f"Compare {a[m]} and {a[j]}.", "compare")
            if a[j] < a[m]:
                m = j
                add_step(s, a, [m], f"New smallest found: {a[m]}! 🔎", "found")
        if m != i:
            a[i], a[m] = a[m], a[i]
            add_step(s, a, [i, m], f"Hoppy swaps {a[m]} and {a[i]}. 🐰", "swap")
        else:
            add_step(s, a, [i], f"{a[i]} is already perfect here. 🌷", "done")
    add_step(s, a, list(range(n)), "All sorted! Tiny happy dance! 🎀", "finish")
    return s

def bubble_steps(arr):
    a = arr.copy(); s = []
    add_step(s, a, [], "Ready for bubble hops! 🫧", "start")
    n = len(a)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            add_step(s, a, [j, j+1], f"Compare neighbors {a[j]} and {a[j+1]}.", "compare")
            if a[j] > a[j+1]:
                left, right = a[j], a[j+1]
                a[j], a[j+1] = a[j+1], a[j]
                swapped = True
                add_step(s, a, [j, j+1], f"Swap {left} and {right}. Bigger one bubbles right! 🫧", "swap")
        if not swapped:
            add_step(s, a, list(range(n)), "No swaps this pass — already sorted! ✨", "finish")
            return s
    add_step(s, a, list(range(n)), "Bubble party complete! 🎀", "finish")
    return s

def insertion_steps(arr):
    a = arr.copy(); s=[]
    add_step(s, a, [0], "First value is our tiny sorted group. 🧩", "start")
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        add_step(s, a, [i], f"Pick up key = {key}. 🐰", "pick")
        while j >= 0 and a[j] > key:
            a[j+1] = a[j]
            add_step(s, a, [j, j+1], f"Slide {a[j]} one spot right.", "shift")
            j -= 1
        a[j+1] = key
        add_step(s, a, [j+1], f"Place {key} into its cozy spot. 🌸", "insert")
    add_step(s, a, list(range(len(a))), "Everything is neatly inserted! 🎀", "finish")
    return s

def merge_steps(arr):
    a = arr.copy(); s=[]
    add_step(s, a, [], "Merge Sort begins by splitting into smaller groups. 🧁", "start")
    def merge_sort(l, r, depth=0):
        if l >= r: return
        m = (l+r)//2
        add_step(s, a, list(range(l, r+1)), f"Split indices {l}..{r} around the middle.", "split")
        merge_sort(l, m, depth+1)
        merge_sort(m+1, r, depth+1)
        left = a[l:m+1]
        right = a[m+1:r+1]
        i=j=0; k=l
        while i < len(left) and j < len(right):
            add_step(s, a, [k], f"Merge: compare {left[i]} and {right[j]}.", "compare")
            if left[i] <= right[j]:
                a[k]=left[i]; i+=1
            else:
                a[k]=right[j]; j+=1
            add_step(s, a, [k], f"Place {a[k]} into the merged section.", "insert")
            k+=1
        while i < len(left):
            a[k]=left[i]; i+=1
            add_step(s, a, [k], f"Copy remaining {a[k]} from the left half.", "insert")
            k+=1
        while j < len(right):
            a[k]=right[j]; j+=1
            add_step(s, a, [k], f"Copy remaining {a[k]} from the right half.", "insert")
            k+=1
        add_step(s, a, list(range(l,r+1)), f"Merged section {l}..{r} is sorted. ✨", "done")
    merge_sort(0, len(a)-1)
    add_step(s, a, list(range(len(a))), "All tiny groups are merged into one sorted line! 🎀", "finish")
    return s

def quick_steps(arr):
    a=arr.copy(); s=[]
    add_step(s, a, [], "Quick Sort chooses a pivot and makes two teams. ⚡", "start")
    def qs(low, high):
        if low >= high: return
        pivot=a[high]
        add_step(s, a, [high], f"Pivot = {pivot}. 🐧", "pivot")
        i=low-1
        for j in range(low, high):
            add_step(s, a, [j, high], f"Compare {a[j]} with pivot {pivot}.", "compare")
            if a[j] <= pivot:
                i += 1
                if i != j:
                    a[i],a[j]=a[j],a[i]
                    add_step(s, a, [i,j], "Move this smaller value into the left team. 🐰", "swap")
        a[i+1],a[high]=a[high],a[i+1]
        p=i+1
        add_step(s, a, [p], f"Pivot {a[p]} lands in its final spot! 🌷", "done")
        qs(low,p-1); qs(p+1,high)
    qs(0,len(a)-1)
    add_step(s,a,list(range(len(a))),"Quick Sort complete! ⚡🎀","finish")
    return s

def recursive_bubble_steps(arr):
    a=arr.copy(); s=[]
    add_step(s,a,[],"Recursive Bubble Sort: bubble once, then call yourself! 🔁","start")
    def rb(n, call_no=1):
        if n == 1:
            add_step(s,a,[0],"Base case: n = 1. Stop recursion. 🌸","done")
            return
        add_step(s,a,list(range(n)),f"Recursive call with n = {n}.","call")
        for i in range(n-1):
            add_step(s,a,[i,i+1],f"Compare {a[i]} and {a[i+1]}.","compare")
            if a[i] > a[i+1]:
                a[i],a[i+1]=a[i+1],a[i]
                add_step(s,a,[i,i+1],"Swap neighbors. 🫧","swap")
        add_step(s,a,[n-1],f"Largest current value is fixed at index {n-1}.","done")
        rb(n-1,call_no+1)
    rb(len(a))
    add_step(s,a,list(range(len(a))),"Recursion finished — sorted! 🎀","finish")
    return s

def recursive_insertion_steps(arr):
    a=arr.copy(); s=[]
    add_step(s,a,[],"Recursive Insertion Sort grows a sorted prefix. 🔁🧩","start")
    def ri(n):
        if n <= 1:
            add_step(s,a,[0],"Base case: first value is already sorted.","done")
            return
        add_step(s,a,list(range(n-1)),f"First sort the first {n-1} values recursively.","call")
        ri(n-1)
        key=a[n-1]
        j=n-2
        add_step(s,a,[n-1],f"Now insert last value {key}. 🐰","pick")
        while j>=0 and a[j] > key:
            a[j+1]=a[j]
            add_step(s,a,[j,j+1],f"Shift {a[j]} right.","shift")
            j-=1
        a[j+1]=key
        add_step(s,a,[j+1],f"Place {key} into its correct spot. 🌷","insert")
    ri(len(a))
    add_step(s,a,list(range(len(a))),"Recursive insertion complete! 🎀","finish")
    return s

STEP_FUNCS = {
    "Selection Sort": selection_steps,
    "Bubble Sort": bubble_steps,
    "Insertion Sort": insertion_steps,
    "Merge Sort": merge_steps,
    "Quick Sort": quick_steps,
    "Recursive Bubble Sort": recursive_bubble_steps,
    "Recursive Insertion Sort": recursive_insertion_steps,
}

def render_animation(name, arr):
    steps = STEP_FUNCS[name](arr)
    safe_steps = json.dumps(steps)
    component = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
body {{
  margin:0;
  font-family: "Trebuchet MS", "Arial Rounded MT Bold", sans-serif;
  background: linear-gradient(145deg,#fffafc,#ffeaf5);
  color:#654f6b;
}}
.wrap {{
  border:2px solid #ffd6e8;
  border-radius:28px;
  padding:18px;
  background:rgba(255,255,255,.88);
  box-shadow:0 10px 26px rgba(220,140,180,.12);
}}
.top {{
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:12px;
  flex-wrap:wrap;
}}
.title {{
  font-weight:900;
  font-size:18px;
}}
.controls button {{
  border:none;
  border-radius:999px;
  padding:9px 14px;
  margin-left:6px;
  background:#ffd8ea;
  color:#6d526f;
  font-weight:900;
  cursor:pointer;
}}
.controls button:hover {{ background:#ffbddb; }}
.scene {{
  position:relative;
  display:flex;
  justify-content:center;
  align-items:flex-end;
  gap:12px;
  min-height:190px;
  padding:42px 8px 16px;
  overflow-x:auto;
}}
.slot {{
  position:relative;
  min-width:64px;
  height:86px;
  border-radius:22px;
  border:2px solid #ffd0e5;
  background:linear-gradient(#fff,#fff0f7);
  display:flex;
  align-items:center;
  justify-content:center;
  font-weight:900;
  font-size:23px;
  box-shadow:0 8px 16px rgba(255,153,196,.10);
  transition:all .28s ease;
}}
.slot.active {{
  transform:translateY(-13px);
  background:linear-gradient(#fff8fc,#ffd8eb);
  border-color:#ff97c3;
  box-shadow:0 12px 22px rgba(255,125,182,.22);
}}
.mascot {{
  position:absolute;
  top:-37px;
  left:50%;
  transform:translateX(-50%);
  font-size:30px;
  animation:hop .65s ease-in-out infinite alternate;
}}
.rabbit {{
  position:absolute;
  right:-11px;
  bottom:-23px;
  font-size:25px;
  animation:wiggle .7s ease-in-out infinite alternate;
}}
@keyframes hop {{
  from {{ transform:translate(-50%,0) rotate(-4deg); }}
  to {{ transform:translate(-50%,-10px) rotate(4deg); }}
}}
@keyframes wiggle {{
  from {{ transform:rotate(-7deg); }}
  to {{ transform:rotate(7deg); }}
}}
.msg {{
  background:#fff7fb;
  border:1.5px dashed #ffb8d7;
  padding:11px 14px;
  border-radius:16px;
  text-align:center;
  font-weight:800;
  min-height:22px;
}}
.progress {{
  margin-top:12px;
  height:9px;
  background:#ffe5f1;
  border-radius:999px;
  overflow:hidden;
}}
.bar {{
  height:100%;
  width:0%;
  background:#ff9ac6;
  transition:width .25s ease;
}}
.small {{
  margin-top:8px;
  text-align:center;
  color:#997b99;
  font-size:12px;
}}
</style>
</head>
<body>
<div class="wrap">
  <div class="top">
    <div class="title">🐧 Sorty + 🐰 Hoppy animation</div>
    <div class="controls">
      <button onclick="prev()">◀ Back</button>
      <button onclick="toggle()" id="playBtn">▶ Play</button>
      <button onclick="next()">Next ▶</button>
      <button onclick="resetAnim()">↺ Reset</button>
    </div>
  </div>
  <div class="scene" id="scene"></div>
  <div class="msg" id="msg"></div>
  <div class="progress"><div class="bar" id="bar"></div></div>
  <div class="small" id="counter"></div>
</div>
<script>
const steps = {safe_steps};
let idx = 0;
let timer = null;

function render() {{
  const s = steps[idx];
  const scene = document.getElementById("scene");
  scene.innerHTML = "";
  s.arr.forEach((v, i) => {{
    const slot = document.createElement("div");
    slot.className = "slot" + (s.active.includes(i) ? " active" : "");
    slot.textContent = v;

    if (s.active.includes(i)) {{
      const p = document.createElement("div");
      p.className = "mascot";
      p.textContent = (i === s.active[0]) ? "🐧" : "🐰";
      slot.appendChild(p);
    }}
    if (s.action === "swap" && s.active.includes(i) && i === s.active[s.active.length-1]) {{
      const r = document.createElement("div");
      r.className = "rabbit";
      r.textContent = "✨";
      slot.appendChild(r);
    }}
    scene.appendChild(slot);
  }});
  document.getElementById("msg").textContent = s.message;
  document.getElementById("counter").textContent = `Step ${{idx+1}} of ${{steps.length}}`;
  document.getElementById("bar").style.width = `${{((idx+1)/steps.length)*100}}%`;
}}

function next() {{
  if (idx < steps.length-1) idx++;
  else idx = 0;
  render();
}}
function prev() {{
  if (idx > 0) idx--;
  render();
}}
function toggle() {{
  const btn = document.getElementById("playBtn");
  if (timer) {{
    clearInterval(timer); timer = null; btn.textContent = "▶ Play";
  }} else {{
    btn.textContent = "⏸ Pause";
    timer = setInterval(() => {{
      if (idx >= steps.length-1) {{
        clearInterval(timer); timer=null; btn.textContent="▶ Play";
      }} else {{
        idx++; render();
      }}
    }}, 900);
  }}
}}
function resetAnim() {{
  if (timer) clearInterval(timer);
  timer=null; idx=0;
  document.getElementById("playBtn").textContent="▶ Play";
  render();
}}
render();
</script>
</body>
</html>
"""
    components.html(component, height=330, scrolling=False)

def complexity_row(name):
    t, s, stable = CONCEPTS[name]["complexity"]
    c1,c2,c3 = st.columns(3)
    c1.markdown(f"<div class='soft-card'><b>⏱ Time</b><br>{t}</div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='soft-card'><b>🎒 Extra Space</b><br>{s}</div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='soft-card'><b>🌷 Stable?</b><br>{stable}</div>", unsafe_allow_html=True)

def home():
    st.markdown("<div class='cute-title'>Sorty & Hoppy's Sorting Garden</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>A tiny pink Java playground where 🐧 Sorty and 🐰 Hoppy make sorting feel less scary.</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="hero-card">
      <div class="mascots">🐧 🌷 🐰</div>
      <h3>Which sort would you like to learn?</h3>
      <p>Pick one card. We’ll explain the idea, animate it, show Java code, and decode the code line by line.</p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(2)
    for idx, algo in enumerate(ALGORITHMS):
        with cols[idx % 2]:
            if st.button(f"{ALGO_EMOJI[algo]}  {algo}", key=f"home_{algo}", use_container_width=True):
                st.session_state.page = algo
                st.rerun()

    st.markdown("""
    <div class="tip-card">
      <b>🌸 Beginner tip:</b> Start with <b>Bubble Sort → Selection Sort → Insertion Sort</b>.
      Then learn Merge Sort and Quick Sort. After that, recursion versions will feel much easier.
    </div>
    """, unsafe_allow_html=True)

def arrays_page():
    top1, top2 = st.columns([1,5])
    with top1:
        if st.button("← Home", key="back_arrays"):
            st.session_state.page="Home"; st.rerun()
    with top2:
        st.markdown("<h1>🥕 Arrays with Hoppy</h1>", unsafe_allow_html=True)

    st.markdown("""
    <div class="concept-card">
      <h3>What is an array?</h3>
      <p>An array is a fixed-size row of boxes. Every box stores one value, and every box has an index.</p>
      <p>🐰 Hoppy remembers: <b>index starts at 0</b>.</p>
    </div>
    """, unsafe_allow_html=True)

    components.html("""
    <div style="font-family:Trebuchet MS;background:#fff9fc;border:2px solid #ffd7e9;border-radius:25px;padding:22px;text-align:center">
      <div style="font-size:34px;margin-bottom:12px">🐰 🥕 🥕 🥕 🥕 🥕</div>
      <div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap">
        <div style="padding:18px;border:2px solid #ffbddb;border-radius:18px;background:white"><b>7</b><br><small>index 0</small></div>
        <div style="padding:18px;border:2px solid #ffbddb;border-radius:18px;background:white"><b>4</b><br><small>index 1</small></div>
        <div style="padding:18px;border:2px solid #ffbddb;border-radius:18px;background:white"><b>1</b><br><small>index 2</small></div>
        <div style="padding:18px;border:2px solid #ffbddb;border-radius:18px;background:white"><b>5</b><br><small>index 3</small></div>
        <div style="padding:18px;border:2px solid #ffbddb;border-radius:18px;background:white"><b>3</b><br><small>index 4</small></div>
      </div>
    </div>
    """, height=185)

    st.subheader("Java basics")
    st.code("""int[] arr = {7, 4, 1, 5, 3};

System.out.println(arr[0]);  // 7

arr[2] = 10;                // change index 2

for (int i = 0; i < arr.length; i++) {
    System.out.println(arr[i]);
}""", language="java")

    st.markdown("""
    <div class="soft-card">
      <span class="pill">arr[0] → first value</span>
      <span class="pill">arr.length → number of values</span>
      <span class="pill">arr[i] → value at index i</span>
      <span class="pill">arr[i] = x → update a value</span>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🐧 Why are arrays important for sorting?"):
        st.write("Sorting algorithms repeatedly **read**, **compare**, **shift**, and **swap** array values. If indexing feels comfortable, sorting code becomes much easier.")

    st.info("Next cute path: Arrays → Bubble Sort → Selection Sort → Insertion Sort 🌸")

def algorithm_page(name):
    top1, top2 = st.columns([1,5])
    with top1:
        if st.button("← Home", key=f"back_{name}"):
            st.session_state.page="Home"; st.rerun()
    with top2:
        st.markdown(f"<h1>{ALGO_EMOJI[name]} {name}</h1>", unsafe_allow_html=True)

    c = CONCEPTS[name]
    st.markdown(f"""
    <div class="concept-card">
      <h3>🌷 The idea in one sentence</h3>
      <p style="font-size:1.08rem"><b>{c["one_liner"]}</b></p>
      <p>{c["story"]}</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🐾 Tiny steps")
    for i, step in enumerate(c["steps"], start=1):
        st.markdown(f"<span class='pill'>{i}. {step}</span>", unsafe_allow_html=True)

    complexity_row(name)

    st.subheader("🎀 Try the animation")
    raw = st.text_input(
        "Type 2–9 integers separated by commas",
        value="7, 4, 1, 5, 3",
        key=f"array_{name}",
        help="Example: 7, 4, 1, 5, 3",
    )
    arr = parse_array(raw)
    if arr is None:
        st.error("Please enter 2–9 whole numbers, like: 7, 4, 1, 5, 3")
        arr = [7,4,1,5,3]
    render_animation(name, arr)

    st.subheader("☕ Java code")
    st.code(JAVA_CODE[name], language="java")

    st.subheader("🐰 Decode the code, gently")
    for snippet, explanation in LINE_EXPLANATIONS[name]:
        st.markdown(
            f"<div class='soft-card'><code>{html.escape(snippet)}</code><br><span>{explanation}</span></div>",
            unsafe_allow_html=True
        )

    with st.expander("🧠 What should I remember for an exam/interview?"):
        if name == "Selection Sort":
            st.write("Selection Sort repeatedly **selects the minimum** from the unsorted part and puts it at the beginning.")
        elif name == "Bubble Sort":
            st.write("Bubble Sort repeatedly **compares adjacent values**. After each pass, the largest unsorted value reaches the end.")
        elif name == "Insertion Sort":
            st.write("Insertion Sort keeps a **sorted left portion** and inserts one new value into its correct position.")
        elif name == "Merge Sort":
            st.write("Merge Sort is **divide and conquer**: split, recursively sort, then merge. Its key complexity is **O(n log n)**.")
        elif name == "Quick Sort":
            st.write("Quick Sort uses a **pivot and partitioning**. Average time is **O(n log n)**, but a bad pivot pattern can cause **O(n²)**.")
        elif name == "Recursive Bubble Sort":
            st.write("Do one normal bubble pass, then recursively sort the first **n - 1** elements. Base case: **n == 1**.")
        elif name == "Recursive Insertion Sort":
            st.write("Recursively sort the first **n - 1**, then insert the nth value into the sorted prefix. Base case: **n <= 1**.")

    st.markdown("<div class='footer'>Made with 🌸 + 🐧 + 🐰 for Java sorting practice.</div>", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "Home"

if st.session_state.page == "Home":
    home()
elif st.session_state.page == "Arrays":
    arrays_page()
else:
    algorithm_page(st.session_state.page)
