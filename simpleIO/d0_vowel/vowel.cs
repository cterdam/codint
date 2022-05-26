class vowel
{
    static void Main()
    {
        string str = System.Console.ReadLine();
        System.Text.StringBuilder sb = new System.Text.StringBuilder(str);
        for (int i = 0; i < sb.Length; i++)
        {
            if ("aeiouAEIOU".Contains(sb[i])) {
                sb[i] = char.ToUpper(sb[i]);
            }
            else
            {
                sb[i] = char.ToLower(sb[i]);
            }
        }
        System.Console.WriteLine(sb.ToString());
    }
}
