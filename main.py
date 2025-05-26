from lexer import tokenize
from parser import Parser
from interpreter import Interpreter

def run(code):
    tokens = tokenize(code)
    tree = Parser(tokens).parse()
    Interpreter().eval(tree)

program = """
ይዘው ድ = 1;
ይዘው ዝ = [10, 20, 30];

አትም(ድ);
አትም(ዝ[1]);

ፋንክሽን ይማር(ሃ) {
    አትም("ሰላም እዚህ ሃ ነው");
    መመለስ ሃ + 1;
}

ይዘው ማ = ይማር(5);
አትም(ማ);

ይዘው ብዛት = 0;
በማዘጋጀት (ብዛት < 3) {
    አትም(ብዛት);
    ብዛት = ብዛት + 1;
}

ለ(ይዘው አ = 0; አ < 5; አ = አ + 1) {
    ድ = ድ + አ;
    አትም(ድ);
}

ከሆነ (ድ > 10) {
    አትም("ድ ከ10 በላይ ነው");
} ካልሆነ {
    አትም("ድ ከ10 በታች ነው");
}

ዝ[1] = 99;
አትም(ዝ[1]);

ይዘው ጣት = ጠይቅ("ቁጥር አስገባ: ");
አትም("ተሰጠ ቁጥር: " + ጣት);

ይዘው flag = ሐሰት;
ከሆነ (flag) {
    አትም("flag is true");
} ካልሆነ {
    አትም("flag is false");
}
"""

run(program)