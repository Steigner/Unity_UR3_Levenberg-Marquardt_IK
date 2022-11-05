using UnityEngine;

public class Joint : MonoBehaviour
{
    // set child joint
    public Joint m_child;

    // check on trigger collision
    void OnTriggerEnter(Collider other)
    {
        Client.is_collision = true;
        string objectName = gameObject.name;
        Debug.Log("Collision detected: " + objectName);
    }
    // get chiled joint
    public Joint GetChild()
    {
        return m_child;
    }
}
