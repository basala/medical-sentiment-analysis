
import gov.nih.nlm.nls.metamap.*;

import java.io.*;
import java.util.List;
import java.util.ArrayList;

/**
 * An example of using the api to read an input file and then writing
 * the result to an output file.
 * <p>
 * Created: Tue May 19 09:42:22 2009
 *
 * @author <a href="mailto:wrogers@nlm.nih.gov">Willie Rogers</a>
 * @version 1.0
 */
public class Run {


  /**
   * Creates a new <code>TestFE</code> instance.
   *
   */
  public Run() {

  }
  
  void process(String inputFilename, String outputFilename )
  {

    try {
      MetaMapApi api = new MetaMapApiImpl(0);

/*      String options ="-y";
      api.setOptions(options);
      System.out.println("Options: " + options);*/
      
      List<Result> resultList = api.processCitationsFromFile(inputFilename);
      
      for (Result result: resultList) {
    	  
	if (result != null) {
	  PrintWriter pw = new PrintWriter(outputFilename);
	  pw.println("result: " + result.getMachineOutput());
	  pw.close();
	}
      }
    } catch (Exception e) {
      System.out.println("Error when querying Prolog Server: " +
			 e.getMessage() + '\n');
    }
  }

  void process2(String inputFilename, String outputFilename)
  {
    try {
      StringBuffer sb = new StringBuffer();
      BufferedReader br = new BufferedReader(new FileReader(inputFilename));
      String line;
      while ((line = br.readLine()) != null) {
	sb.append(line).append("\n");
      }
      br.close();
      String input = sb.toString();
      System.out.println("input: " + input);

      MetaMapApi api = new MetaMapApiImpl(0);
      List<Result> resultList = api.processCitationsFromString(input);
      for (Result result: resultList) {
	if (result != null) {
	  PrintWriter pw = new PrintWriter(outputFilename);
	  List<AcronymsAbbrevs> aaList = result.getAcronymsAbbrevsList();
	  pw.println("Acronyms and Abbreviations:");
	  if (aaList.size() > 0) {
	    for (AcronymsAbbrevs e: aaList) {
	      pw.println("Acronym: " + e.getAcronym());
	      pw.println("Expansion: " + e.getExpansion());
	      pw.println("Count list: " + e.getCountList());
	      pw.println("CUI list: " + e.getCUIList());
	    }
	  } else {
	    pw.println(" None.");
	  }

	  pw.println("Negations:");
	  List<Negation> negList = result.getNegationList();
	  if (negList.size() > 0) {
	    for (Negation e: negList) {
	      pw.println("type: " + e.getType());
	      pw.print("Trigger: " + e.getTrigger() + ": [");
	      for (Position pos: e.getTriggerPositionList()) {
		pw.print(pos  + ",");
	      }
	      pw.println("]");
	      pw.print("ConceptPairs: [");
	      for (ConceptPair pair: e.getConceptPairList()) {
		pw.print(pair + ",");
	      }
	      pw.println("]");
	      pw.print("ConceptPositionList: [");
	      for (Position pos: e.getConceptPositionList()) {
		pw.print(pos + ",");
	      }
	      pw.println("]");
	    }
	  } else {
	    pw.println(" None.");
	  }
	  for (Utterance utterance: result.getUtteranceList()) {
	    pw.println("Utterance:");
	    pw.println(" Id: " + utterance.getId());
	    pw.println(" Utterance text: " + utterance.getString());
	    pw.println(" Position: " + utterance.getPosition());
	  
	    for (PCM pcm: utterance.getPCMList()) {
	      pw.println("Phrase:");
	      pw.println(" text: " + pcm.getPhrase().getPhraseText());

	      pw.println("Candidates:");
	      for (Ev ev: pcm.getCandidateList()) {
		pw.println(" Candidate:");
		pw.println("  Score: " + ev.getScore());
		pw.println("  Concept Id: " + ev.getConceptId());
		pw.println("  Concept Name: " + ev.getConceptName());
		pw.println("  Preferred Name: " + ev.getPreferredName());
		pw.println("  Matched Words: " + ev.getMatchedWords());
		pw.println("  Semantic Types: " + ev.getSemanticTypes());
		pw.println("  is Head?: " + ev.isHead());
		pw.println("  is Overmatch?: " + ev.isOvermatch());
		pw.println("  Sources: " + ev.getSources());
		pw.println("  Positional Info: " + ev.getPositionalInfo());
	      }
	      pw.println("Mappings:");
	      for (Mapping map: pcm.getMappingList()) {
		pw.println(" Mapping:");
		pw.println("  Map Score: " + map.getScore());
		for (Ev mapEv: map.getEvList()) {
		  pw.println("   Score: " + mapEv.getScore());
		  pw.println("   Concept Id: " + mapEv.getConceptId());
		  pw.println("   Concept Name: " + mapEv.getConceptName());
		  pw.println("   Preferred Name: " + mapEv.getPreferredName());
		  pw.println("   Matched Words: " + mapEv.getMatchedWords());
		  pw.println("   Semantic Types: " + mapEv.getSemanticTypes());
		  pw.println("   is Head?: " + mapEv.isHead());
		  pw.println("   is Overmatch?: " + mapEv.isOvermatch());
		  pw.println("   Sources: " + mapEv.getSources());
		  pw.println("   Positional Info: " + mapEv.getPositionalInfo());
		}
	      }
	    }
	  }
	  pw.close();
	} else {
	  System.out.println("NULL result instance! ");
	}
      }
    } catch (Exception e) {
      System.out.println("Error when querying Prolog Server: " +
			 e.getMessage() + '\n');
    }
  }
  
  void MyProcess(String inputFilename, String outputFilename)
  {
    try {
      MetaMapApi api = new MetaMapApiImpl(0); //Instantiating the API
      
      String options ="--prune 20";
      api.setOptions(options);
      System.out.println("Options: " + options);
      
/*      StringBuffer sb = new StringBuffer();
      BufferedReader br = new BufferedReader(new FileReader(inputFilename));*/
      
      FileInputStream fileInput = new FileInputStream(inputFilename);
	  InputStreamReader inputStrReader = new InputStreamReader(fileInput/*,"utf-8"*/);
	  BufferedReader buf = new BufferedReader(inputStrReader);
	  
	  FileOutputStream fileOutput = new FileOutputStream(outputFilename);
      OutputStreamWriter writer = new OutputStreamWriter(fileOutput/*, "utf-8"*/);
	  
      String line;
      int num_line=0;
      while ((line = buf.readLine()) != null) {
    	  ++num_line;
    	  if(num_line%500==0) System.out.print(num_line+"......");
//    	  System.out.println(++num_line);
//    	  System.out.println(line);
          writer.write("textid: "+num_line+"\r\n");
          List<Result> resultList = api.processCitationsFromString(line);

          for (Result result: resultList) {
        	  if (result != null) {
        		  for (Utterance utterance: result.getUtteranceList()) {//utterance按句子划分
		    	    writer.write("Utterance:\r\n");
		    	    writer.write(" Id: " + utterance.getId()+"\r\n");
		    	    writer.write(" Utterance text: " + utterance.getString()+"\r\n");
		    	    writer.write(" Position: " + utterance.getPosition()+"\r\n");
    	  
		    	    for (PCM pcm: utterance.getPCMList()) {
		    	    	writer.write("Phrase:"+"\r\n");
		    	    	writer.write(" text: " + pcm.getPhrase().getPhraseText()+"\r\n");
    	      //mapping
		    	    	writer.write("Mappings:"+"\r\n");
		    	    	for (Mapping map: pcm.getMappingList()) {
		    	    		writer.write("  Map Score: " + map.getScore()+"\r\n");
		    	    		for (Ev mapEv: map.getEvList()) {
				    			writer.write("   Score: " + mapEv.getScore()+"\r\n");
				    			writer.write("   Concept Id: " + mapEv.getConceptId()+"\r\n");
				    			writer.write("   Concept Name: " + mapEv.getConceptName()+"\r\n");
				    			writer.write("   Preferred Name: " + mapEv.getPreferredName()+"\r\n");
				    			writer.write("   Matched Words: " + mapEv.getMatchedWords()+"\r\n");
				    			writer.write("   Semantic Types: " + mapEv.getSemanticTypes()+"\r\n");
				    			writer.write("   Positional Info: " + mapEv.getPositionalInfo()+"\r\n");
		    	    		}
		    	    		break;
		    	    	}
		    	    }
        		  }
        	  } else {
        		  System.out.println("NULL result instance! ");
        	  }
          }
          writer.write("\r\n");
          
      }
      buf.close();
      writer.close();
      System.out.println("done");
       
    } catch (Exception e) {
      System.out.println("Error when querying Prolog Server: " +
			 e.getMessage() + '\n');
    }
  }
  
  public static void main(String[] args) {
    Run frontEnd = new Run();
    
    if (args.length < 2) {
      System.out.println("usage: TestFE <inputfile> <outputfile>");
      System.exit(0);
    }
//    String infile="D:\\PPIAC\\metamap\\input\\test.txt";
//    String outfile="D:\\PPIAC\\metamap\\output\\test.out";
//    frontEnd.MyProcess(infile, outfile);
    frontEnd.MyProcess(args[0], args[1]);
  }
}
