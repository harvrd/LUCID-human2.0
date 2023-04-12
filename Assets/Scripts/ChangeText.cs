using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class ChangeText : MonoBehaviour
{
    public GameObject changingText;
    TextMeshPro thetext;
    // Start is called before the first frame update
    void Start()
    {
        Debug.Log("start");
        thetext = changingText.GetComponent<TextMeshPro>();
        Debug.Log("done");

    }

    // Update is called once per frame
    void Update()
    {

    }
    void Awake()
    {
        Debug.Log("awaken");
    }

    public void ChangeTextTo()
    {
        string newText = "Hello World";
        thetext.text = newText;
        Debug.Log("Text changed to: " + newText);
    }
}
