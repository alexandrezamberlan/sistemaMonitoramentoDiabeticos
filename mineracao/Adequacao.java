import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import javax.swing.JOptionPane;

public class Adequacao {
    public static void lerArquivo() {
        String nomeArquivo;
        try {
            nomeArquivo = JOptionPane.showInputDialog(null, "Nome do arquivo");
            FileReader fr;
            fr = new FileReader(nomeArquivo);
            BufferedReader bf = new BufferedReader(fr);
            String linha;
            String listaLinha[];
            do {
                linha = bf.readLine();
                if (linha == null) {
                    break;
                }
                if (linha.charAt(0) != '@'){
                    listaLinha = linha.split(",");
                }
                if (Integer.parseInt(listaLinha[3]) < 80) {
                    listaLinha[3] = "Abaixo";
                } 
            } while(true);
            bf.close();
        }catch (Exception e){
            System.out.println("Erro "+ e.getMessage());
        }
    }
    public static void main(String a[]) {
        //
    }
}